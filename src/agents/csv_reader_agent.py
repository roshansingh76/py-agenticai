import pandas as pd
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class CSVReaderAgent:
    """Agent responsible for reading and parsing feedback data from CSV files"""
    
    def __init__(self):
        self.name = "CSV Reader Agent"
        logger.info(f"{self.name} initialized")
    
    def read_app_reviews(self, file_path: str) -> List[Dict]:
        """Read app store reviews from CSV file"""
        try:
            df = pd.read_csv(file_path)
            reviews = df.to_dict('records')
            logger.info(f"Read {len(reviews)} app store reviews from {file_path}")
            return reviews
        except Exception as e:
            logger.error(f"Error reading app reviews: {e}")
            raise
    
    def read_support_emails(self, file_path: str) -> List[Dict]:
        """Read support emails from CSV file"""
        try:
            df = pd.read_csv(file_path)
            emails = df.to_dict('records')
            logger.info(f"Read {len(emails)} support emails from {file_path}")
            return emails
        except Exception as e:
            logger.error(f"Error reading support emails: {e}")
            raise
    
    def read_all_feedback(self, reviews_path: str, emails_path: str) -> Dict[str, List[Dict]]:
        """Read all feedback sources"""
        return {
            'reviews': self.read_app_reviews(reviews_path),
            'emails': self.read_support_emails(emails_path)
        }
