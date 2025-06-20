#!/usr/bin/env python3
"""
Test script for real email functionality
"""

import sys
import os
sys.path.append('src')

from function_library import FunctionLibrary

def test_email_sending():
    """Test the real email sending functionality"""
    print("🧪 Testing Real Email Functionality")
    print("=" * 50)
    
    # Initialize function library
    lib = FunctionLibrary()
    
    # Test 1: Email validation
    print("\n1. Testing email validation...")
    result = lib.validate_email("test@example.com")
    print(f"   Valid email check: {result}")
    
    # Test 2: Invalid email validation
    print("\n2. Testing invalid email...")
    result = lib.validate_email("invalid-email")
    print(f"   Invalid email check: {result}")
    
    # Test 3: Send test email (this will try to send a real email)
    print("\n3. Testing real email sending...")
    test_content = {
        "message": "This is a test email from the Smart Function Pipeline",
        "timestamp": "2024-06-21",
        "test_data": [1, 2, 3, 4, 5]
    }
    
    # You can change this email to your own for testing
    test_recipient = "test@example.com"  # Change this to a real email for testing
    
    result = lib.send_email(
        content=test_content,
        recipient=test_recipient,
        subject="Test Email from Smart Function Pipeline"
    )
    print(f"   Email sending result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ Email testing complete!")
    
    # Check environment variables
    print("\n📋 Environment Configuration:")
    print(f"   SMTP Server: {os.getenv('SMTP_SERVER', 'Not set')}")
    print(f"   SMTP Port: {os.getenv('SMTP_PORT', 'Not set')}")
    print(f"   Email Username: {os.getenv('EMAIL_USERNAME', 'Not set')}")
    print(f"   Email Password: {'Set' if os.getenv('EMAIL_PASSWORD') else 'Not set'}")

if __name__ == "__main__":
    test_email_sending()
