from fastapi import APIRouter, Depends
from src.controller.chat_controller import ChatController
from src.models.chat_models import ChatResponse, ChatRequest

router = APIRouter()


def get_controller() -> ChatController:
    """Dependency injection for controller"""
    return ChatController()


@router.get("/basic", response_model=ChatResponse)
async def basic_chat(controller: ChatController = Depends(get_controller)) -> ChatResponse:
    """Get basic chat response"""
    return await controller.handle_basic_chat()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    controller: ChatController = Depends(get_controller)
) -> ChatResponse:
    """Send message and get AI response"""
    return await controller.handle_chat_message(request)
