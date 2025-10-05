#!/usr/bin/env python3
"""
Documentation Downloader - Main Entry Point
This is the main entry point for the Documentation Downloader application.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_dependencies():
    """Check if required dependencies are available"""
    missing_deps = []
    
    try:
        import fastapi
    except ImportError:
        missing_deps.append("fastapi")
    
    try:
        import uvicorn
    except ImportError:
        missing_deps.append("uvicorn")
    
    try:
        import aiofiles
    except ImportError:
        missing_deps.append("aiofiles")
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        missing_deps.append("beautifulsoup4")
    
    return missing_deps

if __name__ == "__main__":
    # Check dependencies first
    missing_deps = check_dependencies()
    
    if missing_deps:
        print("❌ Missing required dependencies:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n💡 Solution:")
        print("   Run the application using the virtual environment:")
        print(f"   {os.path.join(os.path.dirname(__file__), '.venv', 'bin', 'python')} app.py")
        print("\n   Or install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Import version and main function only after dependency check
    from core.version import __version__
    from start_app import main
    
    print(f"Documentation Downloader v{__version__}")
    main()