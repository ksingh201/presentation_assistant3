#!/usr/bin/env python3
import asyncio
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build

from aiohttp import web
from slide_detector import slide_queue
from slides_service import SlidesService
from slide_mapping import mapping
from tts_service import TTSService
from qa_service import QAService

# Will hold slide-index → notes text
notes = {}

async def slide_change(request):
    """Handle GET /slide-change?hash=#slide=<ID>"""
    raw = request.query.get("hash", "")
    if raw.startswith("#slide="):
        new = raw.split("#slide=", 1)[1]
        print(f"[DETECTOR] {raw!r} → {new!r}")
        await slide_queue.put(new)
    return web.Response(
        text="ok",
        headers={"Access-Control-Allow-Origin": "*"}
    )

async def slide_options(request):
    """Reply to OPTIONS for CORS preflight."""
    return web.Response(
        status=200,
        headers={"Access-Control-Allow-Origin": "*"}
    )

async def healthz(request):
    """Health check endpoint for extension polling."""
    return web.Response(
        text="ok",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

async def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    logging.info("=== Presentation Assistant: Notes Stage ===")

    # ——— Load config & Services —————————————————————
    with open("config.json") as f:
        cfg = json.load(f)
    slides_url = cfg.get("slides_url")
    if not slides_url:
        raise RuntimeError("Please set slides_url in config.json")

    slides = SlidesService("google_credentials.json", slides_url)
    tts = TTSService()
    qa = QAService()
    notes = slides.load_all_notes()
    logging.info(f"Loaded {len(notes)} slides worth of notes")

    # ——— Start HTTP server ───────────────────────────────────
    app = web.Application()
    app.add_routes([
        web.get   ("/slide-change", slide_change),
        web.options("/slide-change", slide_options),
        web.get   ("/healthz",       healthz),
    ])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8765)
    await site.start()
    logging.info("Detector listening on http://127.0.0.1:8765")

    # ——— Consume slide events and handle narration & Q&A ─────────────────
    while True:
        obj_id = await slide_queue.get()
        obj_id = obj_id.replace('id.', '')  # Strip the 'id.' prefix
        idx = mapping.update_current_slide(obj_id)
        text = notes.get(idx, "<no notes>")
        print(f"📝 Slide {idx} notes: {text}")
        
        # Narrate the notes using TTS
        if text != "<no notes>":
            await tts.speak(text)
            
            # Q&A for all slides with limited attempts
            print("[QA] Ready for questions about this slide...")
            
            # Initial prompt for questions
            await tts.speak("Any questions about this slide?")
            
            # Allow up to 2 questions per slide
            for _ in range(2):
                try:
                    # Ask for a question (non-blocking)
                    question = await qa.ask_question(timeout=10.0)
                    
                    # Handle different response types
                    if question is None:  # Silence or explicit "no"
                        print("[QA] No questions detected")
                        break
                        
                    # Get answer with slide context
                    answer = await qa.answer(question, text)
                    print(f"[QA] Question: {question}")
                    print(f"[QA] Answer: {answer}")
                    await tts.speak(answer)
                    
                    # Ask if they have more questions
                    await tts.speak("Do you have any other questions about this slide?")
                    more_questions = await qa.ask_question(timeout=5.0)
                    
                    # Handle follow-up response
                    if more_questions is None:
                        print("[QA] No more questions")
                        break
                        
                except Exception as e:
                    logging.error(f"QA error: {e}")
                    await tts.speak("Sorry, I couldn't get an answer right now.")
                    break

if __name__ == "__main__":
    asyncio.run(main())