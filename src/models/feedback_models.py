from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FeedbackInput(BaseModel):
    """Input model for feedback processing"""
    reviews_file: Optional[str] = Field(None, description="Path to reviews CSV file")
    emails_file: Optional[str] = Field(None, description="Path to emails CSV file")


class FeedbackItem(BaseModel):
    """Model for individual feedback item"""
    source_id: str
    source_type: str  # 'review' or 'email'
    text: str
    rating: Optional[int] = None
    platform: Optional[str] = None
    user_name: Optional[str] = None
    date: Optional[str] = None


class ClassificationResult(BaseModel):
    """Model for classification result"""
    source_id: str
    category: str  # Bug, Feature Request, Praise, Complaint, Spam
    confidence: float
    priority: str  # Critical, High, Medium, Low


class TicketResponse(BaseModel):
    """Model for generated ticket"""
    ticket_id: str
    source_id: str
    source_type: str
    category: str
    title: str
    description: str
    priority: str
    status: str
    assigned_to: str
    tags: str
    created_at: str


class ProcessingResult(BaseModel):
    """Model for processing results"""
    total_feedback: int
    tickets_created: int
    tickets_approved: int
    processing_time: float
    category_breakdown: dict


class QualityReview(BaseModel):
    """Model for quality review results"""
    total_tickets: int
    approved: int
    rejected: int
    average_quality_score: float
