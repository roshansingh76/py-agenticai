from openai import AsyncOpenAI
import os
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for OpenAI API integration"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = os.getenv("MODEL_NAME", "gpt-4o-mini")
    
    async def get_chat_response(self, message: str) -> str:
        """Get AI response for a message"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
