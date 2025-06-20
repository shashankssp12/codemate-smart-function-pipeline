#!/usr/bin/env python3
"""
Test script for file download function.
"""

from src.function_library import FunctionLibrary
import os

def test_download_function():
    """Test file download functionality."""
    lib = FunctionLibrary()
    
    print("Testing File Download Function:")
    print("=" * 40)
    
    # Test downloading a small text file
    print("1. Testing File Download:")
    try:
        result = lib.execute_function('download_file', {
            'url': 'https://httpbin.org/robots.txt',
            'filename': 'test_robots.txt'
        })
        print(f"   Download result: {result}")
        
        # Check if file was actually created
        if os.path.exists(result.get('filepath', '')):
            with open(result['filepath'], 'r') as f:
                content = f.read()[:100]
            print(f"   File content preview: {content}...")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 40)
    print("File download test completed!")

if __name__ == "__main__":
    test_download_function()
