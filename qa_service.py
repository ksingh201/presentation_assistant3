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
            "no", "nope", "none", "nothing", "skip",
            "no questions", "no thank you", "no thanks", "not now"
        }

    async def ask_question(self, timeout: float = 5.0) -> str | None:
        """
        Use speech-to-text to get a question from the user.
        
        Returns:
            str: The transcribed question if one was detected
            None: If no audio was detected or on timeout
        Raises:
            Exception: If there was an error with the STT service
        """
        try:
            response = await self.stt.listen(timeout)
            
            # Handle silence/timeout
            if not response or len(response) < 2:
                return None
                
            # Convert to lowercase for comparison
            response = response.lower()
            
            # Check for "no" responses
            if response in self.no_responses:
                return None
                
            # Return the original response (not lowercase)
            return response
            
        except Exception as e:
            # Log the error but let the caller handle it
            raise Exception(f"STT error: {str(e)}")

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