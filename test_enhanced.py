#!/usr/bin/env python3
"""
Test script for the enhanced Documentation Downloader with progress tracking
"""

import asyncio
import requests
import json
import time

def test_basic_functionality():
    """Test basic server functionality"""
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_status_endpoint():
    """Test the status endpoint"""
    try:
        response = requests.get("http://localhost:8000/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status endpoint working: {data}")
            return True
        else:
            print(f"❌ Status endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Enhanced Documentation Downloader")
    print("=" * 50)
    
    # Test basic functionality
    if not test_basic_functionality():
        print("❌ Basic functionality test failed")
        return
    
    # Test status endpoint
    if not test_status_endpoint():
        print("❌ Status endpoint test failed")
        return
    
    print("\n✅ All basic tests passed!")
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://localhost:8000 in your browser")
    print("2. Enter a test URL (e.g., https://httpbin.org/html)")
    print("3. Choose PDF or Markdown format")
    print("4. Click 'Download Documentation'")
    print("5. Watch the progress bar and status messages")
    print("6. Verify the progress shows:")
    print("   - Step 1: Starting documentation download")
    print("   - Step 2: Visiting the URL")
    print("   - Step 3: Extracting documentation")
    print("   - Step 4: Documentation extracted")
    print("   - Step 5: Creating HTML/Markdown")
    print("   - Step 6: File ready")
    print("   - Step 7: Download complete")
    print("\n🎉 Enhanced features ready for testing!")

if __name__ == "__main__":
    main()