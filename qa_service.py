# qa_service.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from stt_service import STTService

load_dotenv()

class QAService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set in .env")
        # Instantiate the new OpenAI client
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
        self.stt = STTService()
        
        # Common variations of "no" responses
        self.no_responses = {
            "no", "nope", "nah", "no questions", "no thank you",
            "no thanks", "not now", "none", "nothing", "skip"
        }

    async def ask_question(self) -> str:
        """
        Use speech-to-text to get a question from the user.
        Returns None if user indicates no questions.
        """
        print("[QA] Listening for a question...")
        response = await self.stt.listen(5.0)  # Listen for 5 seconds
        
        # Check for empty or very short responses
        if not response or len(response) < 2:
            print("[QA] No clear response detected")
            return None
            
        # Check for "no" responses
        if response in self.no_responses:
            print(f"[QA] Detected 'no' response: {response!r}")
            return None
            
        # If we got here, assume it's a real question
        print(f"[QA] Detected question: {response!r}")
        return response

    def get_answer(self, question: str) -> str:
        """
        Get an answer to a question using GPT-4.
        """
        # Synchronous call—no await
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a concise assistant answering slide-related questions."},
                {"role": "user", "content": question}
            ],
            temperature=0.5,
            max_tokens=150,  # Reduced from 200 to 150 for faster responses
        )
        return resp.choices[0].message.content.strip()

    async def answer(self, question: str, context: str) -> str:
        """
        Query GPT-4 with the user question and full slide-context using the
        new synchronous chat API.
        """
        messages = [
            {"role": "system", "content": "You are a concise assistant answering slide-related questions."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
        # Synchronous call—no await
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
            max_tokens=150,  # Reduced from 200 to 150 for faster responses
        )
        return resp.choices[0].message.content.strip()