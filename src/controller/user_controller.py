from fastapi import HTTPException, status
from src.models.user_models import UserResponse, LoginRequest, LoginResponse
import logging

logger = logging.getLogger(__name__)


class UserController:
    """Controller for user operations"""
    
    async def handle_get_current_user(self) -> UserResponse:
        """Get current user info"""
        try:
            # TODO: Get user from JWT token
            return UserResponse(
                user_id="test_user_123",
                email="user@example.com",
                username="testuser"
            )
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to get user"
            )
    
    async def handle_user_login(self, request: LoginRequest) -> LoginResponse:
        """Handle user login"""
        try:
            # TODO: Validate credentials and generate JWT
            return LoginResponse(
                user_id="test_user_123",
                access_token="mock_jwt_token",
                token_type="bearer"
            )
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
