from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def read_user_me():
    return {"user_id": "the current user asdasdas"}
@router.get("/login")
async def read_user_login():
    return {"user_id": "the current user login  "}

