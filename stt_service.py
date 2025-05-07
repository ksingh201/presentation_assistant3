# stt_service.py
import os
import tempfile
import openai
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()

class STTService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in .env")
        openai.api_key = api_key
        self.samplerate = 16000
        self.channels = 1

    def _clean_transcription(self, text: str) -> str:
        """Clean up the transcription text."""
        if not text:
            return ""
        
        # Remove extra whitespace and convert to lowercase
        text = text.strip().lower()
        
        # Remove punctuation except for apostrophes
        text = ''.join(c for c in text if c.isalnum() or c.isspace() or c == "'")
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text

    async def listen(self, timeout: float) -> str:
        # 1) Record audio
        filename = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
        print(f"[STT] Recording {timeout}s to {filename}…")
        recording = sd.rec(int(timeout * self.samplerate),
                         samplerate=self.samplerate,
                         channels=self.channels)
        sd.wait()
        sf.write(filename, recording, self.samplerate)
        print(f"[STT] Saved recording to {filename}")

        # 2) Transcribe via OpenAI's new Audio API
        print("[STT] Transcribing audio…")
        with open(filename, "rb") as f:
            resp = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )
        
        # Clean up the transcription
        text = self._clean_transcription(resp)
        print(f"[STT] Raw transcription: {resp!r}")
        print(f"[STT] Cleaned transcription: {text!r}")
        
        # Clean up the temporary file
        try:
            os.unlink(filename)
        except:
            pass
            
        return text