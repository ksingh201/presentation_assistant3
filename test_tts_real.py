# test_tts_real.py
import asyncio
from tts_service import TTSService

async def main():
    tts = TTSService()
    await tts.speak("Hello, this is a real ElevenLabs test.")

if __name__ == "__main__":
    asyncio.run(main())