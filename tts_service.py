"""
Text-to-Speech service using ElevenLabs.
Handles conversion of text to natural-sounding speech.
"""
# tts_service.py
import os
import asyncio
import tempfile
import subprocess
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

class TTSService:
    def __init__(self):
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise RuntimeError("ELEVENLABS_API_KEY not set in .env")
        self.client   = ElevenLabs(api_key=api_key)
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"
        self.model_id = "eleven_multilingual_v2"

    async def speak(self, text: str):
        """Generate and *play* the TTS audio."""
        # 1) Generate the MP3 bytes
        chunks = self.client.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format="mp3_44100_128"
        )
        audio = b"".join(chunks)

        # 2) Write to a temp file
        tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp.write(audio)
        tmp.flush()
        path = tmp.name
        tmp.close()

        print(f"[TTS] Generated {len(audio)} bytes for: {text!r}")
        print("[TTS] Playing narration…")

        # 3) Play using system player
        # macOS: afplay, Linux: mpg123, Windows: start
        if os.name == "posix" and subprocess.run(["which","afplay"], stdout=subprocess.DEVNULL).returncode == 0:
            await asyncio.to_thread(subprocess.run, ["afplay", path])
        elif os.name == "posix":
            await asyncio.to_thread(subprocess.run, ["mpg123", path])
        else:
            # Windows
            await asyncio.to_thread(subprocess.run, ["powershell", "-c", f"Start-Process '{path}'"])