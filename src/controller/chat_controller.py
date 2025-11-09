from fastapi import HTTPException, status
from src.services.chat_service import ChatService
from src.models.chat_models import ChatResponse, ChatRequest
import logging

logger = logging.getLogger(__name__)


class ChatController:
    """Controller for chat business logic"""
    
    def __init__(self):
        self.chat_service = ChatService()
    
    async def handle_basic_chat(self) -> ChatResponse:
        """Handle basic chat with default message"""
        try:
            message = "Hello, how can I use Py-Agentic AI?"
            response_text = await self.chat_service.get_chat_response(message)
            return ChatResponse(response=response_text)
        except Exception as e:
            logger.error(f"Error in basic chat: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Chat service error"
            )
    
    async def handle_chat_message(self, request: ChatRequest) -> ChatResponse:
        """Handle custom chat message"""
        try:
            if not request.message.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Message cannot be empty"
                )
            
            response_text = await self.chat_service.get_chat_response(request.message)
            return ChatResponse(response=response_text)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Chat service error"
            )

