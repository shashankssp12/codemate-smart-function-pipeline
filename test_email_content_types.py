"""
Test script to verify email functions work with different content types
"""

import sys
import os

# Add the src directory to Python path
sys.path.append('src')

from function_library import FunctionLibrary

def test_email_content_formatting():
    """Test email function with different content types."""
    
    lib = FunctionLibrary()
    
    # Test with dictionary content
    print("Testing send_email with dictionary content...")
    dict_content = {
        "summary": {
            "total_amount": 15500.0,
            "total_count": 3,
            "status_breakdown": {"paid": 2, "pending": 1},
            "average_amount": 5166.67
        }
    }
    
    result = lib.send_email(
        content=dict_content,
        recipient="test@example.com",
        subject="Invoice Summary Report"
    )
    print(f"Dictionary content result: {result}")
    print()
    
    # Test with list content
    print("Testing send_email with list content...")
    list_content = [
        {"invoice_id": "INV-001", "amount": 5000, "status": "paid"},
        {"invoice_id": "INV-002", "amount": 7500, "status": "paid"},
        {"invoice_id": "INV-003", "amount": 3000, "status": "pending"}
    ]
    
    result = lib.send_email(
        content=list_content,
        recipient="test@example.com",
        subject="Invoice List"
    )
    print(f"List content result: {result}")
    print()
    
    # Test with string content
    print("Testing send_email with string content...")
    string_content = "This is a simple string message."
    
    result = lib.send_email(
        content=string_content,
        recipient="test@example.com",
        subject="Simple Message"
    )
    print(f"String content result: {result}")
    print()
    
    # Test helper methods directly
    print("Testing helper methods directly...")
    
    # Test _format_dict_for_email
    formatted_dict = lib._format_dict_for_email(dict_content)
    print(f"Formatted dict:\n{formatted_dict}")
    print()
    
    # Test _format_list_for_email
    formatted_list = lib._format_list_for_email(list_content)
    print(f"Formatted list:\n{formatted_list}")
    print()

if __name__ == "__main__":
    test_email_content_formatting()
