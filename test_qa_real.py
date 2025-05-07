# test_qa_real.py
import asyncio
from qa_service import QAService

async def main():
    qa = QAService()
    answer = await qa.answer(
        "What is two plus two?",
        "Slide 1: simple arithmetic examples."
    )
    print("GPT-4 answered:", answer)

if __name__ == "__main__":
    asyncio.run(main()) 