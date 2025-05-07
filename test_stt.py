# test_stt.py
import asyncio
from stt_service import STTService

async def main():
    resp = await STTService().listen(1.0)
    print("Response:", resp)

if __name__ == "__main__":
    asyncio.run(main()) 