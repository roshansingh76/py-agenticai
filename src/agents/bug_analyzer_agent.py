import logging
import re
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class BugAnalyzerAgent:
    """Agent responsible for extracting technical details from bug reports"""
    
    def __init__(self):
        self.name = "Bug Analysis Agent"
        logger.info(f"{self.name} initialized")
    
    def analyze_bug(self, feedback: Dict) -> Dict:
        """Extract technical details from bug report"""
        text = feedback.get('review_text') or feedback.get('body', '')
        
        analysis = {
            'platform': self._extract_platform(feedback, text),
            'device': self._extract_device(text),
            'os_version': self._extract_os_version(text),
            'app_version': feedback.get('app_version', 'Unknown'),
            'severity': self._assess_severity(text, feedback.get('rating')),
            'steps_to_reproduce': self._extract_steps(text),
            'error_message': self._extract_error_message(text),
            'impact': self._assess_impact(text)
        }
        
        return analysis
    
    def _extract_platform(self, feedback: Dict, text: str) -> str:
        """Extract platform information"""
        platform = feedback.get('platform', '')
        if platform:
            return platform
        
        text_lower = text.lower()
        if 'android' in text_lower:
            return 'Android'
        elif 'ios' in text_lower or 'iphone' in text_lower or 'ipad' in text_lower:
            return 'iOS'
        
        return 'Unknown'
    
    def _extract_device(self, text: str) -> str:
        """Extract device model from text"""
        # Common device patterns
        device_patterns = [
            r'(iPhone \d+\s*Pro\s*Max|iPhone \d+\s*Pro|iPhone \d+)',
            r'(iPad Pro|iPad Air|iPad Mini|iPad)',
            r'(Samsung Galaxy [A-Z]\d+)',
            r'(Pixel \d+\s*Pro|Pixel \d+)',
            r'(OnePlus \d+)',
            r'(Xiaomi [A-Za-z0-9\s]+)'
        ]
        
        for pattern in device_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return 'Unknown'
    
    def _extract_os_version(self, text: str) -> str:
        """Extract OS version from text"""
        # Android version pattern
        android_match = re.search(r'Android\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if android_match:
            return f"Android {android_match.group(1)}"
        
        # iOS version pattern
        ios_match = re.search(r'iOS\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if ios_match:
            return f"iOS {ios_match.group(1)}"
        
        # iPadOS version pattern
        ipad_match = re.search(r'iPadOS\s+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
        if ipad_match:
            return f"iPadOS {ipad_match.group(1)}"
        
        return 'Unknown'
    
    def _assess_severity(self, text: str, rating: Optional[int]) -> str:
        """Assess bug severity"""
        text_lower = text.lower()
        
        # Critical indicators
        critical_keywords = [
            'data loss', 'deleted', 'lost', 'crash', 'won\'t open',
            'can\'t login', 'urgent', 'critical', 'all my data'
        ]
        
        # High severity indicators
        high_keywords = [
            'not working', 'broken', 'fail', 'error', 'constant',
            'every time', 'always', 'unusable'
        ]
        
        if any(keyword in text_lower for keyword in critical_keywords):
            return 'Critical'
        
        if rating and rating == 1:
            return 'High'
        
        if any(keyword in text_lower for keyword in high_keywords):
            return 'High'
        
        return 'Medium'
    
    def _extract_steps(self, text: str) -> str:
        """Extract steps to reproduce"""
        # Look for numbered steps or sequential actions
        steps_pattern = r'(?:steps?|reproduce|how to)[\s:]+(.+?)(?:\.|$)'
        match = re.search(steps_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # Look for action sequences
        action_words = ['open', 'click', 'select', 'try', 'upload', 'download']
        sentences = text.split('.')
        steps = [s.strip() for s in sentences if any(word in s.lower() for word in action_words)]
        
        if steps:
            return ' -> '.join(steps[:3])  # Return first 3 steps
        
        return 'Not specified'
    
    def _extract_error_message(self, text: str) -> str:
        """Extract error messages from text"""
        # Look for quoted error messages
        error_patterns = [
            r'["\']([^"\']*error[^"\']*)["\']',
            r'error[:\s]+([^.]+)',
            r'message[:\s]+([^.]+)'
        ]
        
        for pattern in error_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return 'None'
    
    def _assess_impact(self, text: str) -> str:
        """Assess user impact"""
        text_lower = text.lower()
        
        high_impact = [
            'unusable', 'can\'t use', 'lost data', 'months of work',
            'critical', 'urgent', 'important'
        ]
        
        if any(keyword in text_lower for keyword in high_impact):
            return 'High - Blocking user workflow'
        
        return 'Medium - Degraded user experience'
    
    def analyze_batch(self, feedback_items: list) -> list:
        """Analyze a batch of bug reports"""
        results = []
        for item in feedback_items:
            if item.get('category') == 'Bug':
                analysis = self.analyze_bug(item)
                results.append({
                    **item,
                    'technical_analysis': analysis
                })
            else:
                results.append(item)
        
        logger.info(f"Analyzed {sum(1 for r in results if 'technical_analysis' in r)} bug reports")
        return results
