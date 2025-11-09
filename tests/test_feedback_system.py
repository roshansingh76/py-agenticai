"""
Comprehensive test suite for Feedback Analysis System
"""
import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('.'))

from src.services.feedback_service import FeedbackService
from src.controller.feedback_controller import FeedbackController


class TestFeedbackService:
    """Test FeedbackService class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = FeedbackService()
    
    def test_service_initialization(self):
        """Test service initializes correctly"""
        assert self.service is not None
        assert self.service.ticket_counter == 1000
        assert isinstance(self.service.processing_log, list)
    
    def test_classify_bug(self):
        """Test bug classification"""
        text = "App crashes when I try to upload photos"
        result = self.service.classify_feedback(text, rating=1)
        
        assert result['category'] == 'Bug'
        assert result['confidence'] > 0
    
    def test_classify_feature(self):
        """Test feature request classification"""
        text = "Please add dark mode feature to the app"
        result = self.service.classify_feedback(text, rating=4)
        
        assert result['category'] == 'Feature Request'
        assert result['confidence'] > 0
    
    def test_classify_praise(self):
        """Test praise classification"""
        text = "Amazing app! Love the new features. Excellent work!"
        result = self.service.classify_feedback(text, rating=5)
        
        assert result['category'] == 'Praise'
        assert result['confidence'] > 0
    
    def test_classify_complaint(self):
        """Test complaint classification"""
        text = "Too expensive. Poor customer service. Disappointed."
        result = self.service.classify_feedback(text, rating=2)
        
        assert result['category'] in ['Complaint', 'Bug']
    
    def test_classify_spam(self):
        """Test spam detection"""
        text = "Buy cheap watches at www.fakewatches.com! Click here!"
        result = self.service.classify_feedback(text)
        
        assert result['category'] == 'Spam'
    
    def test_analyze_bug(self):
        """Test bug analysis"""
        feedback = {
            'platform': 'Android',
            'app_version': '2.1.3'
        }
        text = "App crashes on Samsung Galaxy S21, Android 13"
        
        analysis = self.service.analyze_bug(feedback, text)
        
        assert analysis['platform'] == 'Android'
        assert 'Samsung Galaxy S21' in analysis['device']
        assert analysis['severity'] in ['Critical', 'High']
    
    def test_extract_feature(self):
        """Test feature extraction"""
        text = "Please add calendar integration with Google Calendar"
        
        extraction = self.service.extract_feature(text)
        
        assert 'calendar' in extraction['requested_feature'].lower()
        assert extraction['estimated_demand'] in ['High', 'Medium']
    
    def test_create_ticket(self):
        """Test ticket creation"""
        feedback = {
            'review_id': 'R001',
            'review_text': 'App crashes',
            'rating': 1,
            'platform': 'Android'
        }
        classification = {'category': 'Bug', 'confidence': 0.8}
        analysis = {'platform': 'Android', 'device': 'Unknown', 'severity': 'High', 'app_version': '2.1.3'}
        
        ticket = self.service.create_ticket(feedback, classification, analysis)
        
        assert ticket['ticket_id'].startswith('TICK-')
        assert ticket['category'] == 'Bug'
        assert ticket['priority'] in ['Critical', 'High', 'Medium', 'Low']
        assert ticket['status'] == 'Open'
        assert 'Engineering Team' in ticket['assigned_to']


class TestFeedbackController:
    """Test FeedbackController class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.controller = FeedbackController()
    
    def test_controller_initialization(self):
        """Test controller initializes correctly"""
        assert self.controller is not None
        assert self.controller.feedback_service is not None


class TestIntegration:
    """Integration tests"""
    
    def test_full_pipeline(self):
        """Test complete feedback processing pipeline"""
        service = FeedbackService()
        
        # Check if test data exists
        reviews_path = "data/app_store_reviews.csv"
        emails_path = "data/support_emails.csv"
        
        if not os.path.exists(reviews_path) or not os.path.exists(emails_path):
            pytest.skip("Test data files not found")
        
        # Process feedback
        result = service.process_all_feedback(reviews_path, emails_path)
        
        # Verify results
        assert 'tickets' in result
        assert 'metrics' in result
        assert result['metrics']['total_feedback'] > 0
        assert result['metrics']['tickets_created'] > 0
        assert len(result['tickets']) == result['metrics']['tickets_created']
        
        # Verify ticket structure
        if result['tickets']:
            ticket = result['tickets'][0]
            required_fields = [
                'ticket_id', 'source_id', 'source_type', 'category',
                'title', 'description', 'priority', 'status',
                'assigned_to', 'tags', 'created_at', 'confidence'
            ]
            for field in required_fields:
                assert field in ticket


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
