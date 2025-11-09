import logging
import pandas as pd
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service for processing feedback through multi-agent pipeline"""
    
    def __init__(self):
        self.processing_log = []
        self.ticket_counter = 1000
    
    def read_feedback(self, reviews_path: str, emails_path: str) -> Dict:
        """Read feedback from CSV files"""
        try:
            reviews_df = pd.read_csv(reviews_path)
            emails_df = pd.read_csv(emails_path)
            
            reviews = reviews_df.to_dict('records')
            emails = emails_df.to_dict('records')
            
            logger.info(f"Read {len(reviews)} reviews and {len(emails)} emails")
            return {
                'reviews': reviews,
                'emails': emails,
                'total': len(reviews) + len(emails)
            }
        except Exception as e:
            logger.error(f"Error reading feedback: {e}")
            raise
    
    def classify_feedback(self, text: str, rating: int = None) -> Dict:
        """Classify feedback into categories"""
        text_lower = text.lower()
        
        # Bug detection
        bug_keywords = ['crash', 'bug', 'error', 'broken', 'not working', 'issue', 
                       'fail', 'freeze', 'slow', 'lag', 'data loss']
        bug_score = sum(1 for kw in bug_keywords if kw in text_lower)
        
        # Feature request detection
        feature_keywords = ['feature', 'request', 'add', 'would love', 'please add',
                           'suggestion', 'improve', 'need', 'want', 'integration']
        feature_score = sum(1 for kw in feature_keywords if kw in text_lower)
        
        # Praise detection
        praise_keywords = ['love', 'amazing', 'great', 'excellent', 'perfect', 
                          'best', 'awesome', 'fantastic', 'thank you']
        praise_score = sum(1 for kw in praise_keywords if kw in text_lower)
        
        # Complaint detection
        complaint_keywords = ['expensive', 'price', 'poor', 'bad', 'terrible',
                             'disappointed', 'frustrating', 'customer service']
        complaint_score = sum(1 for kw in complaint_keywords if kw in text_lower)
        
        # Spam detection
        spam_keywords = ['buy', 'cheap', 'www.', 'http', 'click here', 'guaranteed']
        spam_score = sum(1 for kw in spam_keywords if kw in text_lower)
        
        # Check for gibberish
        words = text.split()
        if len(words) > 0:
            meaningful = sum(1 for w in words if len(w) > 3 and any(c in 'aeiouAEIOU' for c in w))
            if meaningful / len(words) < 0.3:
                return {'category': 'Spam', 'confidence': 0.9}
        
        # Determine category
        scores = {
            'Bug': bug_score * (1.5 if rating and rating <= 2 else 1),
            'Feature Request': feature_score,
            'Praise': praise_score * (1.5 if rating and rating >= 4 else 1),
            'Complaint': complaint_score,
            'Spam': spam_score
        }
        
        category = max(scores, key=scores.get)
        confidence = min(scores[category] / 10, 1.0)
        
        return {'category': category, 'confidence': confidence}
    
    def analyze_bug(self, feedback: Dict, text: str) -> Dict:
        """Extract technical details from bug report"""
        import re
        
        # Extract platform
        platform = feedback.get('platform', 'Unknown')
        if not platform or platform == 'Unknown':
            if 'android' in text.lower():
                platform = 'Android'
            elif 'ios' in text.lower() or 'iphone' in text.lower():
                platform = 'iOS'
        
        # Extract device
        device_patterns = [
            r'(iPhone \d+\s*Pro\s*Max|iPhone \d+\s*Pro|iPhone \d+)',
            r'(Samsung Galaxy [A-Z]\d+)',
            r'(Pixel \d+)',
        ]
        device = 'Unknown'
        for pattern in device_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                device = match.group(1)
                break
        
        # Assess severity
        critical_keywords = ['data loss', 'deleted', 'lost', 'crash', 'won\'t open', 'can\'t login']
        severity = 'Critical' if any(kw in text.lower() for kw in critical_keywords) else 'High'
        
        return {
            'platform': platform,
            'device': device,
            'severity': severity,
            'app_version': feedback.get('app_version', 'Unknown')
        }
    
    def extract_feature(self, text: str) -> Dict:
        """Extract feature request details"""
        text_lower = text.lower()
        
        # Identify feature
        feature_patterns = {
            'calendar integration': ['calendar', 'google calendar', 'outlook'],
            'offline mode': ['offline', 'without internet'],
            'dark mode': ['dark mode', 'dark theme', 'night mode'],
            'export functionality': ['export', 'pdf', 'csv'],
            'widget support': ['widget', 'home screen'],
            'biometric auth': ['biometric', 'face id', 'fingerprint'],
        }
        
        feature = 'Feature request'
        for feat, keywords in feature_patterns.items():
            if any(kw in text_lower for kw in keywords):
                feature = feat
                break
        
        # Estimate demand
        high_demand = ['really need', 'must have', 'essential', 'critical']
        demand = 'High' if any(kw in text_lower for kw in high_demand) else 'Medium'
        
        return {
            'requested_feature': feature,
            'estimated_demand': demand
        }
    
    def create_ticket(self, feedback: Dict, classification: Dict, analysis: Dict = None) -> Dict:
        """Create structured ticket"""
        self.ticket_counter += 1
        
        source_type = 'review' if 'review_id' in feedback else 'email'
        source_id = feedback.get('review_id') or feedback.get('email_id')
        text = feedback.get('review_text') or feedback.get('body', '')
        category = classification['category']
        
        # Generate title
        if category == 'Bug':
            platform = analysis.get('platform', 'Unknown') if analysis else 'Unknown'
            title = f"[BUG] Application issue on {platform}"
        elif category == 'Feature Request':
            feature = analysis.get('requested_feature', 'Feature request') if analysis else 'Feature request'
            title = f"[FEATURE] {feature}"
        elif category == 'Complaint':
            title = f"[FEEDBACK] User complaint"
        elif category == 'Praise':
            title = f"[PRAISE] Positive feedback"
        else:
            title = f"[{category.upper()}] User feedback"
        
        # Generate description
        description = f"**Original Feedback:**\n{text}\n\n"
        
        if category == 'Bug' and analysis:
            description += "**Technical Details:**\n"
            description += f"- Platform: {analysis.get('platform', 'Unknown')}\n"
            description += f"- Device: {analysis.get('device', 'Unknown')}\n"
            description += f"- Severity: {analysis.get('severity', 'Unknown')}\n"
            description += f"- App Version: {analysis.get('app_version', 'Unknown')}\n"
        
        if category == 'Feature Request' and analysis:
            description += "**Feature Details:**\n"
            description += f"- Requested: {analysis.get('requested_feature', 'N/A')}\n"
            description += f"- Demand: {analysis.get('estimated_demand', 'Medium')}\n"
        
        # Add source info
        if source_type == 'review':
            description += f"\n**Source:** App Store Review (Rating: {feedback.get('rating', 'N/A')})\n"
        else:
            description += f"\n**Source:** Support Email\n"
        
        # Determine priority
        if category == 'Bug':
            severity = analysis.get('severity', 'Medium') if analysis else 'Medium'
            priority = 'Critical' if severity == 'Critical' else 'High'
        elif category == 'Feature Request':
            demand = analysis.get('estimated_demand', 'Medium') if analysis else 'Medium'
            priority = 'High' if demand == 'High' else 'Medium'
        else:
            priority = 'Low'
        
        # Assign team
        team_mapping = {
            'Bug': 'Engineering Team',
            'Feature Request': 'Product Team',
            'Complaint': 'Customer Success Team',
            'Praise': 'Marketing Team',
            'Spam': 'Moderation Team'
        }
        
        return {
            'ticket_id': f"TICK-{self.ticket_counter}",
            'source_id': source_id,
            'source_type': source_type,
            'category': category,
            'title': title,
            'description': description,
            'priority': priority,
            'status': 'Open',
            'assigned_to': team_mapping.get(category, 'Triage Team'),
            'tags': category.lower().replace(' ', '-'),
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'confidence': classification['confidence']
        }
    
    def process_all_feedback(self, reviews_path: str, emails_path: str) -> Dict:
        """Process all feedback through pipeline"""
        start_time = datetime.now()
        
        # Read feedback
        feedback_data = self.read_feedback(reviews_path, emails_path)
        all_feedback = feedback_data['reviews'] + feedback_data['emails']
        
        # Process each item
        tickets = []
        metrics = {
            'total_feedback': len(all_feedback),
            'bugs': 0,
            'features': 0,
            'praise': 0,
            'complaints': 0,
            'spam': 0,
            'tickets_created': 0
        }
        
        for item in all_feedback:
            text = item.get('review_text') or item.get('body', '')
            rating = item.get('rating')
            
            # Classify
            classification = self.classify_feedback(text, rating)
            category = classification['category']
            
            # Update metrics
            if category == 'Bug':
                metrics['bugs'] += 1
            elif category == 'Feature Request':
                metrics['features'] += 1
            elif category == 'Praise':
                metrics['praise'] += 1
            elif category == 'Complaint':
                metrics['complaints'] += 1
            elif category == 'Spam':
                metrics['spam'] += 1
            
            # Skip spam
            if category == 'Spam':
                continue
            
            # Analyze based on category
            analysis = None
            if category == 'Bug':
                analysis = self.analyze_bug(item, text)
            elif category == 'Feature Request':
                analysis = self.extract_feature(text)
            
            # Create ticket
            ticket = self.create_ticket(item, classification, analysis)
            tickets.append(ticket)
        
        metrics['tickets_created'] = len(tickets)
        metrics['processing_time'] = (datetime.now() - start_time).total_seconds()
        
        logger.info(f"Processed {len(all_feedback)} feedback items, created {len(tickets)} tickets")
        
        return {
            'tickets': tickets,
            'metrics': metrics
        }
    
    def save_tickets(self, tickets: List[Dict], output_path: str):
        """Save tickets to CSV"""
        df = pd.DataFrame(tickets)
        df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(tickets)} tickets to {output_path}")
