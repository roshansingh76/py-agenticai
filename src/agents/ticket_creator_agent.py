import logging
import pandas as pd
from datetime import datetime
from typing import Dict, List

logger = logging.getLogger(__name__)


class TicketCreatorAgent:
    """Agent responsible for creating structured tickets"""
    
    def __init__(self):
        self.name = "Ticket Creator Agent"
        logger.info(f"{self.name} initialized")
        self.ticket_counter = 1000
    
    def create_ticket(self, feedback: Dict) -> Dict:
        """Create a structured ticket from feedback"""
        self.ticket_counter += 1
        
        category = feedback.get('category', 'Unknown')
        source_type = 'review' if 'review_id' in feedback else 'email'
        source_id = feedback.get('review_id') or feedback.get('email_id')
        
        ticket = {
            'ticket_id': f"TICK-{self.ticket_counter}",
            'source_id': source_id,
            'source_type': source_type,
            'category': category,
            'title': self._generate_title(feedback),
            'description': self._generate_description(feedback),
            'priority': self._determine_priority(feedback),
            'status': 'Open',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'assigned_to': self._assign_team(category),
            'tags': self._generate_tags(feedback),
            'metadata': self._extract_metadata(feedback)
        }
        
        return ticket
    
    def _generate_title(self, feedback: Dict) -> str:
        """Generate ticket title"""
        category = feedback.get('category', 'Unknown')
        
        if category == 'Bug':
            analysis = feedback.get('technical_analysis', {})
            platform = analysis.get('platform', 'Unknown')
            
            # Extract key issue from text
            text = feedback.get('review_text') or feedback.get('body', '')
            issue = self._extract_key_issue(text)
            
            return f"[BUG] {issue} on {platform}"
        
        elif category == 'Feature Request':
            feature_analysis = feedback.get('feature_analysis', {})
            feature = feature_analysis.get('requested_feature', 'Feature request')
            return f"[FEATURE] {feature}"
        
        elif category == 'Complaint':
            text = feedback.get('review_text') or feedback.get('subject', 'User complaint')
            return f"[FEEDBACK] {text[:50]}"
        
        elif category == 'Praise':
            return f"[PRAISE] Positive user feedback"
        
        else:
            return f"[{category.upper()}] User feedback"
    
    def _extract_key_issue(self, text: str) -> str:
        """Extract key issue from bug report"""
        text_lower = text.lower()
        
        # Common issue patterns
        if 'crash' in text_lower:
            return 'App crashes'
        elif 'login' in text_lower:
            return 'Login issue'
        elif 'slow' in text_lower or 'performance' in text_lower:
            return 'Performance issue'
        elif 'data' in text_lower and ('loss' in text_lower or 'deleted' in text_lower):
            return 'Data loss'
        elif 'sync' in text_lower:
            return 'Sync failure'
        elif 'battery' in text_lower:
            return 'Battery drain'
        elif 'notification' in text_lower:
            return 'Notification issue'
        elif 'attach' in text_lower or 'upload' in text_lower:
            return 'File attachment issue'
        
        return 'Application error'
    
    def _generate_description(self, feedback: Dict) -> str:
        """Generate detailed ticket description"""
        text = feedback.get('review_text') or feedback.get('body', '')
        category = feedback.get('category')
        
        description = f"**Original Feedback:**\n{text}\n\n"
        
        if category == 'Bug':
            analysis = feedback.get('technical_analysis', {})
            description += "**Technical Details:**\n"
            description += f"- Platform: {analysis.get('platform', 'Unknown')}\n"
            description += f"- Device: {analysis.get('device', 'Unknown')}\n"
            description += f"- OS Version: {analysis.get('os_version', 'Unknown')}\n"
            description += f"- App Version: {analysis.get('app_version', 'Unknown')}\n"
            description += f"- Severity: {analysis.get('severity', 'Unknown')}\n"
            description += f"- Impact: {analysis.get('impact', 'Unknown')}\n"
            
            if analysis.get('error_message') != 'None':
                description += f"- Error Message: {analysis.get('error_message')}\n"
            
            if analysis.get('steps_to_reproduce') != 'Not specified':
                description += f"\n**Steps to Reproduce:**\n{analysis.get('steps_to_reproduce')}\n"
        
        elif category == 'Feature Request':
            feature_analysis = feedback.get('feature_analysis', {})
            description += "**Feature Details:**\n"
            description += f"- Requested Feature: {feature_analysis.get('requested_feature')}\n"
            description += f"- User Benefit: {feature_analysis.get('user_benefit')}\n"
            description += f"- Estimated Demand: {feature_analysis.get('estimated_demand')}\n"
            description += f"- Implementation Complexity: {feature_analysis.get('implementation_complexity')}\n"
        
        # Add source information
        source_type = 'review' if 'review_id' in feedback else 'email'
        if source_type == 'review':
            description += f"\n**Source:** App Store Review (Rating: {feedback.get('rating', 'N/A')})\n"
            description += f"**User:** {feedback.get('user_name', 'Anonymous')}\n"
            description += f"**Date:** {feedback.get('date', 'Unknown')}\n"
        else:
            description += f"\n**Source:** Support Email\n"
            description += f"**From:** {feedback.get('sender_email', 'Unknown')}\n"
            description += f"**Subject:** {feedback.get('subject', 'N/A')}\n"
        
        return description
    
    def _determine_priority(self, feedback: Dict) -> str:
        """Determine ticket priority"""
        category = feedback.get('category')
        
        if category == 'Bug':
            analysis = feedback.get('technical_analysis', {})
            severity = analysis.get('severity', 'Medium')
            
            if severity == 'Critical':
                return 'Critical'
            elif severity == 'High':
                return 'High'
            else:
                return 'Medium'
        
        elif category == 'Feature Request':
            feature_analysis = feedback.get('feature_analysis', {})
            demand = feature_analysis.get('estimated_demand', 'Medium')
            
            if demand == 'High':
                return 'High'
            elif demand == 'Medium-High':
                return 'Medium'
            else:
                return 'Low'
        
        elif category == 'Complaint':
            # Check if it's about support response
            text = (feedback.get('review_text') or feedback.get('body', '')).lower()
            if 'no response' in text or 'customer service' in text:
                return 'High'
            return 'Medium'
        
        else:
            return 'Low'
    
    def _assign_team(self, category: str) -> str:
        """Assign ticket to appropriate team"""
        team_mapping = {
            'Bug': 'Engineering Team',
            'Feature Request': 'Product Team',
            'Complaint': 'Customer Success Team',
            'Praise': 'Marketing Team',
            'Spam': 'Moderation Team'
        }
        return team_mapping.get(category, 'Triage Team')
    
    def _generate_tags(self, feedback: Dict) -> str:
        """Generate tags for ticket"""
        tags = []
        
        category = feedback.get('category')
        tags.append(category.lower().replace(' ', '-'))
        
        if category == 'Bug':
            analysis = feedback.get('technical_analysis', {})
            platform = analysis.get('platform', '').lower()
            if platform:
                tags.append(platform)
            
            severity = analysis.get('severity', '').lower()
            if severity:
                tags.append(severity)
        
        elif category == 'Feature Request':
            tags.append('enhancement')
        
        return ', '.join(tags)
    
    def _extract_metadata(self, feedback: Dict) -> str:
        """Extract metadata as JSON string"""
        metadata = {
            'confidence': feedback.get('confidence', 0),
            'source_rating': feedback.get('rating'),
            'app_version': feedback.get('app_version')
        }
        return str(metadata)
    
    def create_batch(self, feedback_items: List[Dict]) -> List[Dict]:
        """Create tickets for a batch of feedback"""
        tickets = []
        for item in feedback_items:
            # Skip spam
            if item.get('category') != 'Spam':
                ticket = self.create_ticket(item)
                tickets.append(ticket)
        
        logger.info(f"Created {len(tickets)} tickets")
        return tickets
    
    def save_tickets_to_csv(self, tickets: List[Dict], output_path: str):
        """Save tickets to CSV file"""
        df = pd.DataFrame(tickets)
        df.to_csv(output_path, index=False)
        logger.info(f"Saved {len(tickets)} tickets to {output_path}")
