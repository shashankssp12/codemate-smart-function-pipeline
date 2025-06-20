#!/usr/bin/env python3
"""
Test script specifically for web functions including web summarizer and file download.
"""

from src.function_library import FunctionLibrary

def test_web_functions():
    """Test web-related functions."""
    lib = FunctionLibrary()
    
    print("Testing Web Functions:")
    print("=" * 40)
    
    # Test URL status check
    print("1. Testing URL Status Check:")
    status = lib.execute_function('check_url_status', {'url': 'https://httpbin.org/get'})
    print(f"   Status for httpbin.org: {status}")
    
    # Test domain extraction
    print("\n2. Testing Domain Extraction:")
    domain = lib.execute_function('extract_domain', {'url': 'https://www.example.com/path/to/page'})
    print(f"   Domain extracted: {domain}")
    
    # Test web summarizer with a simple URL
    print("\n3. Testing Web Summarizer:")
    try:
        summary = lib.execute_function('web_summarizer', {'url': 'https://httpbin.org/html'})
        print(f"   Summary: {summary['summary'][:100]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 40)
    print("Web function tests completed!")

if __name__ == "__main__":
    test_web_functions()
