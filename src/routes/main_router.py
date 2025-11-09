from fastapi import APIRouter
from src.routes.user_router import router as user_router
from src.routes.chat_router import router as chat_router
from src.routes.feedback_router import router as feedback_router

router = APIRouter()

router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(chat_router, prefix="/mainchat", tags=["Chat"])
router.include_router(feedback_router, prefix="/feedback", tags=["Feedback Analysis"])
