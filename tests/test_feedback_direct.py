"""
Direct test of feedback service without HTTP server
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('.'))

from src.services.feedback_service import FeedbackService
import json


def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_feedback_service():
    """Test feedback service directly"""
    
    print_section("Feedback Analysis System - Direct Test")
    
    # Initialize service
    print("\n🔧 Initializing Feedback Service...")
    service = FeedbackService()
    print("✅ Service initialized")
    
    # Check if data files exist
    reviews_path = "data/app_store_reviews.csv"
    emails_path = "data/support_emails.csv"
    
    if not os.path.exists(reviews_path):
        print(f"❌ Error: {reviews_path} not found")
        return
    
    if not os.path.exists(emails_path):
        print(f"❌ Error: {emails_path} not found")
        return
    
    print(f"✅ Data files found")
    
    # Process feedback
    print_section("Processing Feedback")
    print("🔄 Processing feedback through multi-agent pipeline...")
    
    try:
        result = service.process_all_feedback(reviews_path, emails_path)
        
        print("\n✅ Processing Complete!")
        
        # Display metrics
        metrics = result['metrics']
        print_section("Metrics")
        print(f"📊 Total Feedback: {metrics['total_feedback']}")
        print(f"🎫 Tickets Created: {metrics['tickets_created']}")
        print(f"⏱️  Processing Time: {metrics['processing_time']:.2f}s")
        
        print(f"\n📋 Category Breakdown:")
        print(f"  🐛 Bugs: {metrics['bugs']}")
        print(f"  ✨ Features: {metrics['features']}")
        print(f"  👍 Praise: {metrics['praise']}")
        print(f"  😞 Complaints: {metrics['complaints']}")
        print(f"  🚫 Spam: {metrics['spam']}")
        
        # Display sample tickets
        tickets = result['tickets']
        print_section("Sample Tickets")
        
        for i, ticket in enumerate(tickets[:5], 1):
            print(f"\n🎫 Ticket {i}:")
            print(f"  ID: {ticket['ticket_id']}")
            print(f"  Title: {ticket['title']}")
            print(f"  Category: {ticket['category']}")
            print(f"  Priority: {ticket['priority']}")
            print(f"  Assigned To: {ticket['assigned_to']}")
            print(f"  Confidence: {ticket['confidence']:.2f}")
        
        if len(tickets) > 5:
            print(f"\n... and {len(tickets) - 5} more tickets")
        
        # Save tickets
        print_section("Saving Output")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = f"{output_dir}/generated_tickets.csv"
        service.save_tickets(tickets, output_path)
        print(f"✅ Saved {len(tickets)} tickets to {output_path}")
        
        # Priority breakdown
        print_section("Priority Analysis")
        priority_counts = {}
        for ticket in tickets:
            priority = ticket['priority']
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        for priority, count in sorted(priority_counts.items()):
            print(f"  {priority}: {count}")
        
        # Category breakdown
        print_section("Category Analysis")
        category_counts = {}
        for ticket in tickets:
            category = ticket['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        for category, count in sorted(category_counts.items()):
            print(f"  {category}: {count}")
        
        print_section("Test Complete! ✅")
        print(f"\n📁 Output saved to: {output_dir}/")
        print(f"📊 Total tickets: {len(tickets)}")
        print(f"⚡ Processing speed: {metrics['total_feedback'] / metrics['processing_time']:.1f} items/sec")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_feedback_service()
