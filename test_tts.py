# test_tts.py
import asyncio
from tts_service import TTSService

async def main():
    await TTSService().speak("Hello, this is a TTS stub.")

if __name__ == "__main__":
    asyncio.run(main()) 