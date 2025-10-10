from fastapi import APIRouter
from src.controller.user_controller import get_user_me, get_user_login

router = APIRouter()

@router.get("/me")
async def read_user_me():
    return get_user_me()

@router.get("/login")
async def read_user_login():
    return get_user_login()

