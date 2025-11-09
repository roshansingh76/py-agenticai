import logging
from typing import Dict, Tuple
import re

logger = logging.getLogger(__name__)


class FeedbackClassifierAgent:
    """Agent responsible for classifying feedback into categories"""
    
    CATEGORIES = ['Bug', 'Feature Request', 'Praise', 'Complaint', 'Spam']
    
    def __init__(self):
        self.name = "Feedback Classifier Agent"
        logger.info(f"{self.name} initialized")
        
        # Keywords for classification
        self.bug_keywords = [
            'crash', 'bug', 'error', 'broken', 'not working', 'issue', 'problem',
            'fail', 'freeze', 'slow', 'lag', 'glitch', 'stuck', 'won\'t', 'can\'t',
            'doesn\'t work', 'stopped working', 'data loss', 'deleted', 'missing'
        ]
        
        self.feature_keywords = [
            'feature', 'request', 'add', 'would love', 'please add', 'suggestion',
            'improve', 'enhancement', 'would be nice', 'missing', 'need', 'want',
            'integration', 'support for', 'ability to'
        ]
        
        self.praise_keywords = [
            'love', 'amazing', 'great', 'excellent', 'perfect', 'best', 'awesome',
            'fantastic', 'wonderful', 'thank you', 'appreciate', 'outstanding',
            'brilliant', 'superb', 'incredible'
        ]
        
        self.complaint_keywords = [
            'expensive', 'price', 'cost', 'poor', 'bad', 'terrible', 'worst',
            'disappointed', 'frustrating', 'annoying', 'unacceptable', 'no response',
            'customer service', 'support'
        ]
        
        self.spam_keywords = [
            'buy', 'cheap', 'www.', 'http', 'click here', 'limited time',
            'guaranteed', 'free money', 'winner'
        ]
    
    def classify_feedback(self, text: str, rating: int = None) -> Tuple[str, float]:
        """
        Classify feedback text into a category
        
        Returns:
            Tuple of (category, confidence_score)
        """
        text_lower = text.lower()
        
        # Check for spam first
        spam_score = self._calculate_score(text_lower, self.spam_keywords)
        if spam_score > 0.3 or self._is_gibberish(text):
            return 'Spam', spam_score
        
        # Calculate scores for each category
        bug_score = self._calculate_score(text_lower, self.bug_keywords)
        feature_score = self._calculate_score(text_lower, self.feature_keywords)
        praise_score = self._calculate_score(text_lower, self.praise_keywords)
        complaint_score = self._calculate_score(text_lower, self.complaint_keywords)
        
        # Adjust scores based on rating if available
        if rating is not None:
            if rating <= 2:
                bug_score *= 1.5
                complaint_score *= 1.3
            elif rating >= 4:
                praise_score *= 1.5
        
        # Determine category with highest score
        scores = {
            'Bug': bug_score,
            'Feature Request': feature_score,
            'Praise': praise_score,
            'Complaint': complaint_score
        }
        
        category = max(scores, key=scores.get)
        confidence = scores[category]
        
        logger.debug(f"Classified as {category} with confidence {confidence:.2f}")
        return category, confidence
    
    def _calculate_score(self, text: str, keywords: list) -> float:
        """Calculate score based on keyword matches"""
        matches = sum(1 for keyword in keywords if keyword in text)
        return min(matches / len(keywords), 1.0)
    
    def _is_gibberish(self, text: str) -> bool:
        """Check if text is gibberish/random characters"""
        # Check for excessive consonants or random patterns
        words = text.split()
        if len(words) < 3:
            return False
        
        # Check for meaningful words
        meaningful_words = sum(1 for word in words if len(word) > 3 and self._has_vowels(word))
        return meaningful_words / len(words) < 0.3
    
    def _has_vowels(self, word: str) -> bool:
        """Check if word has vowels"""
        return any(char in 'aeiouAEIOU' for char in word)
    
    def classify_batch(self, feedback_items: list) -> list:
        """Classify a batch of feedback items"""
        results = []
        for item in feedback_items:
            text = item.get('review_text') or item.get('body', '')
            rating = item.get('rating')
            category, confidence = self.classify_feedback(text, rating)
            
            results.append({
                **item,
                'category': category,
                'confidence': confidence
            })
        
        logger.info(f"Classified {len(results)} feedback items")
        return results
