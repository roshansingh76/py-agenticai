from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat endpoints"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")


class ChatResponse(BaseModel):
    """Response model for chat endpoints"""
    response: str = Field(..., description="AI response message")


class ErrorResponse(BaseModel):
    """Standard error response model"""
    detail: str = Field(..., description="Error message")
