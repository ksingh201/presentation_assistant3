# test_qa.py
import asyncio
from qa_service import QAService

async def main():
    resp = await QAService().answer("What is the meaning of life?", "any context")
    print("Answer:", resp)

if __name__ == "__main__":
    asyncio.run(main()) 