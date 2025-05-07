# test_audio_cue_real.py
import asyncio
from audio_cue import play_chime

async def main():
    print("About to play chime…")
    await play_chime()
    print("Chime playback complete.")

if __name__ == "__main__":
    asyncio.run(main()) 