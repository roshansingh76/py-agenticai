from fastapi import APIRouter, Depends, UploadFile, File, Query
from src.controller.feedback_controller import FeedbackController
from typing import Optional
import os

router = APIRouter()


def get_controller() -> FeedbackController:
    """Dependency injection for feedback controller"""
    return FeedbackController()


@router.post("/process")
async def process_feedback(controller: FeedbackController = Depends(get_controller)) -> dict:
    """Process feedback from default CSV files"""
    reviews_path = "data/app_store_reviews.csv"
    emails_path = "data/support_emails.csv"
    
    result = await controller.process_feedback_files(reviews_path, emails_path)
    return result


@router.post("/process/upload")
async def process_uploaded_feedback(
    reviews_file: UploadFile = File(...),
    emails_file: UploadFile = File(...),
    controller: FeedbackController = Depends(get_controller)
) -> dict:
    """Process feedback from uploaded CSV files"""
    result = await controller.process_uploaded_files(reviews_file, emails_file)
    return result


@router.get("/summary")
async def get_summary(controller: FeedbackController = Depends(get_controller)) -> dict:
    """Get processing summary"""
    reviews_path = "data/app_store_reviews.csv"
    emails_path = "data/support_emails.csv"
    
    result = await controller.process_feedback_files(reviews_path, emails_path)
    summary = await controller.get_processing_summary(result)
    
    return summary


@router.get("/tickets")
async def get_tickets(
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    controller: FeedbackController = Depends(get_controller)
) -> dict:
    """Get generated tickets with optional filtering"""
    reviews_path = "data/app_store_reviews.csv"
    emails_path = "data/support_emails.csv"
    
    result = await controller.process_feedback_files(reviews_path, emails_path)
    tickets = await controller.get_tickets(result, category, priority)
    
    return {'total': len(tickets), 'tickets': tickets}


@router.post("/tickets/export")
async def export_tickets(
    output_path: str = Query("output/generated_tickets.csv"),
    controller: FeedbackController = Depends(get_controller)
) -> dict:
    """Export generated tickets to CSV file"""
    reviews_path = "data/app_store_reviews.csv"
    emails_path = "data/support_emails.csv"
    
    result = await controller.process_feedback_files(reviews_path, emails_path)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_result = await controller.save_tickets_to_file(result, output_path)
    
    return save_result


@router.get("/health")
async def health_check() -> dict:
    """Health check for feedback system"""
    return {
        'status': 'healthy',
        'service': 'Feedback Analysis System',
        'agents': ['CSV Reader', 'Classifier', 'Bug Analyzer', 'Feature Extractor', 'Ticket Creator']
    }
