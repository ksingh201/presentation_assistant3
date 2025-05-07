"""
Main entry point for the Presentation Assistant.
This module will coordinate all services and handle the main application flow.
"""
# main.py

import asyncio
import time
from config_loader import SLIDES_URL, GOOGLE_CREDENTIALS_PATH
from slides_service import SlidesService
from slide_detector import run_detector
from slide_mapping import mapping
from tts_service import TTSService
from qa_service import QAService

async def main():
    print("=== Starting Presentation Assistant ===")

    # Initialize services
    slides = SlidesService(GOOGLE_CREDENTIALS_PATH, SLIDES_URL)
    tts = TTSService()
    qa = QAService()

    # Load all slide notes
    notes = slides.load_all_notes()
    print(f"Loaded {len(notes)} slide notes")

    # Start slide detector in background
    detector_task = asyncio.create_task(run_detector())

    # Track last narrated slide to avoid repeats
    last_narrated = 0

    # Main loop
    while True:
        # Get current slide index
        current = mapping.current_slide_index
        print(f"[DEBUG] Detected slide index: {current}")

        # If we have notes for this slide and haven't narrated it yet
        if current in notes and current != last_narrated:
            # Get the notes text
            text = notes[current]
            if text:
                # Generate and play TTS
                print(f"[TTS] Generating audio for slide {current}...")
                await tts.speak(text)

                # For slides 5 and above, engage in Q&A
                if current >= 5:
                    print("[QA] Engaging in Q&A...")
                    await tts.speak("Any questions?")
                    question = await qa.ask_question()
                    if question:  # Only process if we got a real question
                        print(f"[QA] Question: {question}")
                        answer = await qa.answer(question, "\n".join(notes.values()))
                        if answer:
                            print(f"[QA] Answer: {answer}")
                            await tts.speak(answer)
                    else:
                        print("[QA] No questions asked, moving to next slide")

                last_narrated = current

        # Small delay to avoid CPU spinning
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())