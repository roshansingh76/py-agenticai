from fastapi import APIRouter
from src.routes.user import router as user_router
from src.routes.chat import router as chat_router   

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(chat_router, prefix="/chat", tags=["Chat"])