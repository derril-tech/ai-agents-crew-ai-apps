#!/usr/bin/env python3
"""
Debug script to test the API endpoint and identify 500 error
"""

import requests
import json

def test_api_endpoint():
    """Test the API endpoint directly"""
    try:
        # Test the pipeline complete endpoint
        project_id = "ai-powered-voice-controlled-smart-home-manager"
        url = f"http://localhost:8001/api/pipeline-complete/{project_id}"
        
        print(f"Testing URL: {url}")
        
        response = requests.get(url)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Success! Report generated successfully")
            data = response.json()
            print(f"Report keys: {list(data.keys())}")
            if "deliverables" in data:
                print(f"Deliverables keys: {list(data['deliverables'].keys())}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response text: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server not running on port 8001")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_api_endpoint()

