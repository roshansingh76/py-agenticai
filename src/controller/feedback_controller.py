from fastapi import HTTPException, status, UploadFile
from src.services.feedback_service import FeedbackService
from src.models.feedback_models import ProcessingResult
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


class FeedbackController:
    """Controller for feedback processing operations"""
    
    def __init__(self):
        self.feedback_service = FeedbackService()
    
    async def process_feedback_files(self, reviews_path: str, emails_path: str) -> dict:
        """Process feedback from file paths"""
        try:
            # Validate files exist
            if not os.path.exists(reviews_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Reviews file not found: {reviews_path}"
                )
            
            if not os.path.exists(emails_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Emails file not found: {emails_path}"
                )
            
            logger.info(f"Processing feedback from {reviews_path} and {emails_path}")
            
            # Process through service
            result = self.feedback_service.process_all_feedback(reviews_path, emails_path)
            
            logger.info(f"Processing completed: {result['metrics']['tickets_created']} tickets created")
            
            return result
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing feedback: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process feedback: {str(e)}"
            )
    
    async def process_uploaded_files(self, reviews_file: UploadFile, emails_file: UploadFile) -> dict:
        """Process feedback from uploaded files"""
        try:
            # Save uploaded files temporarily
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as reviews_temp:
                reviews_content = await reviews_file.read()
                reviews_temp.write(reviews_content)
                reviews_temp_path = reviews_temp.name
            
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.csv') as emails_temp:
                emails_content = await emails_file.read()
                emails_temp.write(emails_content)
                emails_temp_path = emails_temp.name
            
            try:
                # Process files
                result = self.feedback_service.process_all_feedback(reviews_temp_path, emails_temp_path)
                
                return result
            finally:
                # Clean up temp files
                os.unlink(reviews_temp_path)
                os.unlink(emails_temp_path)
                
        except Exception as e:
            logger.error(f"Error processing uploaded files: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process uploaded files: {str(e)}"
            )
    
    async def get_processing_summary(self, result: dict) -> dict:
        """Get processing summary"""
        try:
            metrics = result['metrics']
            tickets = result['tickets']
            
            # Calculate additional stats
            priority_breakdown = {}
            category_breakdown = {}
            
            for ticket in tickets:
                priority = ticket['priority']
                category = ticket['category']
                
                priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
                category_breakdown[category] = category_breakdown.get(category, 0) + 1
            
            summary = {
                'total_feedback': metrics['total_feedback'],
                'tickets_created': metrics['tickets_created'],
                'processing_time': f"{metrics['processing_time']:.2f}s",
                'category_breakdown': {
                    'bugs': metrics['bugs'],
                    'features': metrics['features'],
                    'praise': metrics['praise'],
                    'complaints': metrics['complaints'],
                    'spam': metrics['spam']
                },
                'priority_breakdown': priority_breakdown,
                'tickets_by_category': category_breakdown
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate summary"
            )
    
    async def get_tickets(self, result: dict, category: str = None, priority: str = None) -> list:
        """Get tickets with optional filtering"""
        try:
            tickets = result['tickets']
            
            # Apply filters
            if category:
                tickets = [t for t in tickets if t['category'] == category]
            
            if priority:
                tickets = [t for t in tickets if t['priority'] == priority]
            
            return tickets
            
        except Exception as e:
            logger.error(f"Error getting tickets: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve tickets"
            )
    
    async def save_tickets_to_file(self, result: dict, output_path: str):
        """Save tickets to CSV file"""
        try:
            tickets = result['tickets']
            self.feedback_service.save_tickets(tickets, output_path)
            
            return {
                'message': f'Saved {len(tickets)} tickets to {output_path}',
                'file_path': output_path,
                'ticket_count': len(tickets)
            }
            
        except Exception as e:
            logger.error(f"Error saving tickets: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save tickets"
            )
