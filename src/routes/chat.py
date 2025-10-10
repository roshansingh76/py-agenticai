from fastapi import APIRouter
from pydantic import BaseModel
from src.controller.chat_controller import user_chat

router = APIRouter()

class ChatPrompt(BaseModel):
   prompt: str

@router.post("/chat")
async def chat(body: ChatPrompt):
   return user_chat(body.prompt)