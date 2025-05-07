# audio_cue.py
import asyncio
import os
from playsound import playsound

CHIME_PATH = os.path.join(os.path.dirname(__file__), "chime.mp3")

async def play_chime():
    """
    Play the chime.mp3 audio cue.
    Uses asyncio.to_thread to avoid blocking the event loop.
    """
    if not os.path.exists(CHIME_PATH):
        raise FileNotFoundError(f"Chime file not found: {CHIME_PATH}")
    print("[CHIME] Playing audio cue…")
    # Run playsound in a thread so we don’t block the asyncio loop
    await asyncio.to_thread(playsound, CHIME_PATH)