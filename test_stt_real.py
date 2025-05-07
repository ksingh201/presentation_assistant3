# test_stt_real.py
import asyncio
from stt_service import STTService

async def main():
    stt = STTService()
    print("Please speak for 3 seconds now…")
    text = await stt.listen(3.0)
    print("You said:", text)

if __name__ == "__main__":
    asyncio.run(main()) 