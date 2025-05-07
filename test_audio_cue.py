# test_audio_cue.py
import asyncio
from audio_cue import play_chime

async def main():
    await play_chime()

if __name__ == "__main__":
    asyncio.run(main()) 