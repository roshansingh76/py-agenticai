import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


class QualityCriticAgent:
    """Agent responsible for reviewing ticket quality and completeness"""
    
    def __init__(self):
        self.name = "Quality Critic Agent"
        logger.info(f"{self.name} initialized")
    
    def review_ticket(self, ticket: Dict) -> Tuple[bool, List[str], int]:
        """
        Review ticket for quality and completeness
        
        Returns:
            Tuple of (is_approved, issues, quality_score)
        """
        issues = []
        quality_score = 100
        
        # Check required fields
        required_fields = ['ticket_id', 'title', 'description', 'priority', 'category']
        for field in required_fields:
            if not ticket.get(field):
                issues.append(f"Missing required field: {field}")
                quality_score -= 20
        
        # Check title quality
        title = ticket.get('title', '')
        if len(title) < 10:
            issues.append("Title too short (minimum 10 characters)")
            quality_score -= 10
        elif len(title) > 100:
            issues.append("Title too long (maximum 100 characters)")
            quality_score -= 5
        
        if not title.startswith('['):
            issues.append("Title should start with category tag (e.g., [BUG])")
            quality_score -= 5
        
        # Check description quality
        description = ticket.get('description', '')
        if len(description) < 50:
            issues.append("Description too short (minimum 50 characters)")
            quality_score -= 15
        
        if '**Original Feedback:**' not in description:
            issues.append("Description missing original feedback section")
            quality_score -= 10
        
        # Check priority validity
        valid_priorities = ['Critical', 'High', 'Medium', 'Low']
        if ticket.get('priority') not in valid_priorities:
            issues.append(f"Invalid priority. Must be one of: {', '.join(valid_priorities)}")
            quality_score -= 10
        
        # Category-specific checks
        category = ticket.get('category', '')
        
        if category == 'Bug':
            if '**Technical Details:**' not in description:
                issues.append("Bug ticket missing technical details section")
                quality_score -= 15
            
            # Check for platform info
            if 'Platform:' not in description:
                issues.append("Bug ticket missing platform information")
                quality_score -= 10
        
        elif category == 'Feature Request':
            if '**Feature Details:**' not in description:
                issues.append("Feature request missing feature details section")
                quality_score -= 15
        
        # Check assignment
        if not ticket.get('assigned_to'):
            issues.append("Ticket not assigned to any team")
            quality_score -= 10
        
        # Check tags
        if not ticket.get('tags'):
            issues.append("Ticket missing tags")
            quality_score -= 5
        
        # Determine approval
        is_approved = quality_score >= 70 and len(issues) == 0
        
        return is_approved, issues, max(0, quality_score)
    
    def review_batch(self, tickets: List[Dict]) -> Dict:
        """Review a batch of tickets"""
        results = {
            'total_tickets': len(tickets),
            'approved': 0,
            'rejected': 0,
            'tickets_with_issues': [],
            'average_quality_score': 0
        }
        
        total_score = 0
        
        for ticket in tickets:
            is_approved, issues, quality_score = self.review_ticket(ticket)
            total_score += quality_score
            
            if is_approved:
                results['approved'] += 1
            else:
                results['rejected'] += 1
                results['tickets_with_issues'].append({
                    'ticket_id': ticket.get('ticket_id'),
                    'issues': issues,
                    'quality_score': quality_score
                })
        
        results['average_quality_score'] = total_score / len(tickets) if tickets else 0
        
        logger.info(f"Reviewed {len(tickets)} tickets: {results['approved']} approved, {results['rejected']} rejected")
        logger.info(f"Average quality score: {results['average_quality_score']:.2f}")
        
        return results
    
    def generate_quality_report(self, review_results: Dict) -> str:
        """Generate a quality report"""
        report = "=== QUALITY REVIEW REPORT ===\n\n"
        report += f"Total Tickets Reviewed: {review_results['total_tickets']}\n"
        report += f"Approved: {review_results['approved']}\n"
        report += f"Rejected: {review_results['rejected']}\n"
        report += f"Average Quality Score: {review_results['average_quality_score']:.2f}/100\n\n"
        
        if review_results['tickets_with_issues']:
            report += "=== TICKETS WITH ISSUES ===\n\n"
            for ticket_issue in review_results['tickets_with_issues']:
                report += f"Ticket ID: {ticket_issue['ticket_id']}\n"
                report += f"Quality Score: {ticket_issue['quality_score']}/100\n"
                report += "Issues:\n"
                for issue in ticket_issue['issues']:
                    report += f"  - {issue}\n"
                report += "\n"
        
        return report
