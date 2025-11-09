import logging
import re
from typing import Dict

logger = logging.getLogger(__name__)


class FeatureExtractorAgent:
    """Agent responsible for extracting feature requests and estimating impact"""
    
    def __init__(self):
        self.name = "Feature Extractor Agent"
        logger.info(f"{self.name} initialized")
    
    def extract_feature(self, feedback: Dict) -> Dict:
        """Extract feature request details"""
        text = feedback.get('review_text') or feedback.get('body', '')
        
        extraction = {
            'requested_feature': self._identify_feature(text),
            'user_benefit': self._extract_benefit(text),
            'estimated_demand': self._estimate_demand(feedback),
            'implementation_complexity': self._estimate_complexity(text),
            'similar_requests': 0  # Would be calculated by comparing with other requests
        }
        
        return extraction
    
    def _identify_feature(self, text: str) -> str:
        """Identify the requested feature"""
        text_lower = text.lower()
        
        # Common feature patterns
        feature_patterns = {
            'calendar integration': ['calendar', 'google calendar', 'outlook', 'scheduling'],
            'offline mode': ['offline', 'without internet', 'no connectivity'],
            'dark mode': ['dark mode', 'dark theme', 'night mode', 'oled'],
            'export functionality': ['export', 'pdf', 'csv', 'download'],
            'widget support': ['widget', 'home screen', 'quick access'],
            'biometric auth': ['biometric', 'face id', 'fingerprint', 'touch id'],
            'cloud integration': ['google drive', 'dropbox', 'cloud storage', 'onedrive'],
            'search improvements': ['search', 'find', 'filter', 'advanced search'],
            'collaboration': ['share', 'collaborate', 'team', 'multi-user'],
            'templates': ['template', 'recurring', 'preset']
        }
        
        for feature, keywords in feature_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return feature
        
        # Extract from common request patterns
        request_patterns = [
            r'(?:add|implement|include)\s+([^.!?]+)',
            r'(?:would love|would like|want|need)\s+(?:to see|to have)?\s*([^.!?]+)',
            r'(?:please|could you)\s+add\s+([^.!?]+)'
        ]
        
        for pattern in request_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip()[:50]  # Limit length
        
        return 'Feature request (details in description)'
    
    def _extract_benefit(self, text: str) -> str:
        """Extract user benefit from feature request"""
        text_lower = text.lower()
        
        # Look for benefit indicators
        benefit_patterns = [
            r'(?:would|will)\s+(?:make|be|help)([^.!?]+)',
            r'(?:so that|because|since)([^.!?]+)',
            r'(?:useful|helpful|great|perfect)\s+for\s+([^.!?]+)'
        ]
        
        for pattern in benefit_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1).strip()
        
        return 'Improved user experience'
    
    def _estimate_demand(self, feedback: Dict) -> str:
        """Estimate user demand for feature"""
        rating = feedback.get('rating', 3)
        text = feedback.get('review_text') or feedback.get('body', '')
        text_lower = text.lower()
        
        # High demand indicators
        high_demand_keywords = [
            'really need', 'must have', 'essential', 'critical',
            'many users', 'everyone', 'all users'
        ]
        
        if any(keyword in text_lower for keyword in high_demand_keywords):
            return 'High'
        
        if rating >= 4:
            return 'Medium-High'
        
        return 'Medium'
    
    def _estimate_complexity(self, text: str) -> str:
        """Estimate implementation complexity"""
        text_lower = text.lower()
        
        # Complex features
        complex_keywords = [
            'integration', 'sync', 'real-time', 'collaboration',
            'multi-user', 'cloud', 'api'
        ]
        
        # Simple features
        simple_keywords = [
            'button', 'color', 'theme', 'font', 'icon',
            'notification', 'reminder'
        ]
        
        if any(keyword in text_lower for keyword in complex_keywords):
            return 'High'
        
        if any(keyword in text_lower for keyword in simple_keywords):
            return 'Low'
        
        return 'Medium'
    
    def extract_batch(self, feedback_items: list) -> list:
        """Extract features from a batch of feedback"""
        results = []
        for item in feedback_items:
            if item.get('category') == 'Feature Request':
                extraction = self.extract_feature(item)
                results.append({
                    **item,
                    'feature_analysis': extraction
                })
            else:
                results.append(item)
        
        logger.info(f"Extracted {sum(1 for r in results if 'feature_analysis' in r)} feature requests")
        return results
