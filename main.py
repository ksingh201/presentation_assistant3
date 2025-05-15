#!/usr/bin/env python3
import asyncio
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build

from aiohttp import web
from slide_detector import slide_queue  # re-use your existing queue
from slides_service import SlidesService
from slide_mapping import mapping

# Will hold slide-index → notes text
notes = {}

def get_slide_notes(presentation_id):
    creds = service_account.Credentials.from_service_account_file(
        'google_credentials.json',
        scopes=['https://www.googleapis.com/auth/presentations.readonly']
    )
    service = build('slides', 'v1', credentials=creds)
    presentation = service.presentations().get(presentationId=presentation_id).execute()
    slides = presentation.get('slides', [])
    slide_notes = []
    for i, slide in enumerate(slides, 1):
        notes_text = ""
        if 'slideProperties' in slide and 'notesPage' in slide['slideProperties']:
            notes_page = slide['slideProperties']['notesPage']
            if 'pageElements' in notes_page:
                for element in notes_page['pageElements']:
                    notes_text += extract_text_from_element(element)
        notes_text = ' '.join(notes_text.split())
        slide_notes.append((i, notes_text))
    return slide_notes

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

    # ——— Load config & SlidesService —————————————————————
    with open("config.json") as f:
        cfg = json.load(f)
    slides_url = cfg.get("slides_url")
    if not slides_url:
        raise RuntimeError("Please set slides_url in config.json")

    slides = SlidesService("google_credentials.json", slides_url)
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

    # ——— Consume slide events and print notes ─────────────────
    while True:
        obj_id = await slide_queue.get()
        obj_id = obj_id.replace('id.', '')  # Strip the 'id.' prefix
        idx = mapping.update_current_slide(obj_id)  # Use update_current_slide instead of get
        text = notes.get(idx, "<no notes>")
        print(f"📝 Slide {idx} notes: {text}")

if __name__ == "__main__":
    asyncio.run(main())