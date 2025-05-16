#!/usr/bin/env python3
import asyncio
import logging

from slide_detector import run_detector
# from slides_service import SlidesService
# from tts_service import TTSService
# from stt_service import STTService
# from qa_service import QAService

async def main():
    # ——— Setup logging —————————————————————
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] %(message)s'
    )
    logging.info("=== Starting Presentation Assistant (Test Mode) ===")

    # ——— Original setup (commented out) ——————————————————
    # with open("config.json", "r") as f:
    #     cfg = json.load(f)
    # slides_url = cfg.get("slides_url")
    # slides = SlidesService(slides_url, "google_credentials.json")
    # notes_dict = slides.get_slide_notes()
    # logging.info(f"Loaded {len(notes_dict)} slide notes")
    #
    # tts = TTSService()
    # stt = STTService()
    # qa  = QAService()

    # ——— Start the slide-change detector ——————————————————
    slide_queue = await run_detector()
    logging.info("Slide detector listening on http://127.0.0.1:8765")

    # ——— Wait for one slide event —————————————————————
    slide_id = await slide_queue.get()
    print(f"✅ Received slide change: {slide_id}")

    # ——— The rest of your loop (commented out) ——————————
    # while True:
    #     slide_obj_id = await slide_queue.get()
    #     index = slides.slide_id_to_index(slide_obj_id)
    #     raw_notes = notes_dict.get(index, "")
    #
    #     # Narration
    #     audio_bytes = tts.generate_audio(raw_notes)
    #     tts.play_audio(audio_bytes)
    #
    #     # Q&A stub
    #     if index >= 5:
    #         tts.play_chime()
    #         question = stt.listen(timeout=10.0)
    #         if not question:
    #             tts.speak("Any questions on this slide?")
    #             question = stt.listen(timeout=5.0)
    #         if question:
    #             answer = qa.get_answer(question, context=raw_notes)
    #             tts.speak(answer)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Presentation Assistant terminated by user")