
import os
from fastapi import HTTPException, status
from src.services.chat_service import ChatService
from dotenv import load_dotenv
load_dotenv()

def user_chat(prompt: str):
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="OPENAI_API_KEY environment variable is not set."
		)
	try:
		chat_service = ChatService(api_key=api_key)
		response = chat_service.chat(prompt)
		return {"message": response}
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Chat service error: {str(e)}"
		)
