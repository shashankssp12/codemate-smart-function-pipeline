#!/usr/bin/env python3
"""
Test the actual server endpoint with the problematic query.
"""

import requests
import json

def test_server_endpoint():
    """Test the problematic query through the server."""
    
    print("🧪 Testing Server Endpoint with Invoice Pipeline...")
    print("=" * 60)
    
    # The exact query that's causing issues
    query = "get invoice of march month, summarize it and send it on mail to nitishsr14@gmail.com"
    
    try:
        # Test the server endpoint
        response = requests.post(
            "http://localhost:5000/execute",
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Server Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ HTTP Error {response.status_code}:")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_server_endpoint()
