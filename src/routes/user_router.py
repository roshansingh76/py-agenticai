from fastapi import APIRouter, Depends
from src.controller.user_controller import UserController
from src.models.user_models import UserResponse, LoginRequest, LoginResponse

router = APIRouter()


def get_controller() -> UserController:
    """Dependency injection for controller"""
    return UserController()


@router.get("/me", response_model=UserResponse)
async def get_current_user(controller: UserController = Depends(get_controller)) -> UserResponse:
    """Get current user information"""
    return await controller.handle_get_current_user()


@router.post("/login", response_model=LoginResponse)
async def user_login(
    request: LoginRequest,
    controller: UserController = Depends(get_controller)
) -> LoginResponse:
    """User login endpoint"""
    return await controller.handle_user_login(request)
