from langchain_openai import OpenAI
from langchain.schema import LLMResult
from typing import Optional

class ChatService:
    """
    Service for connecting to OpenAI via LangChain for chat completions.
    """
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        self.llm = OpenAI(openai_api_key=api_key, model_name=model)

    def chat(self, prompt: str) -> str:
        """
        Send a prompt to OpenAI and return the response.
        """
        return self.llm(prompt)

    def chat_with_metadata(self, prompt: str) -> LLMResult:
        """
        Send a prompt and return the full LLMResult (including metadata).
        """
        return self.llm.generate([prompt])
