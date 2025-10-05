#!/usr/bin/env python3
"""
Production-ready run script for Documentation Downloader
"""

import os
import sys
import argparse
import uvicorn
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available"""
    
    # Map package names to import names
    package_imports = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'requests': 'requests',
        'beautifulsoup4': 'bs4',
        'markdownify': 'markdownify',
        'aiofiles': 'aiofiles',
        'jinja2': 'jinja2',
        'python-slugify': 'slugify'
    }
    
    missing_packages = []
    
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_directories():
    """Create necessary directories"""
    
    directories = ['downloads', 'templates', 'static']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    """Main function"""
    
    parser = argparse.ArgumentParser(description='Documentation Downloader')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload for development')
    parser.add_argument('--workers', type=int, default=1, help='Number of worker processes')
    parser.add_argument('--log-level', default='info', choices=['debug', 'info', 'warning', 'error'], help='Log level')
    parser.add_argument('--check', action='store_true', help='Check dependencies and exit')
    
    args = parser.parse_args()
    
    print("🚀 Documentation Downloader")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    if args.check:
        print("✅ All dependencies are available")
        sys.exit(0)
    
    # Setup directories
    setup_directories()
    print("✅ Directories created/verified")
    
    # Import the app
    try:
        from main import app
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        sys.exit(1)
    
    print(f"✅ Application loaded")
    print(f"🌐 Starting server on http://{args.host}:{args.port}")
    print("📚 Access the web interface to download documentation")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Start the server
    try:
        uvicorn.run(
            "main:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers,
            log_level=args.log_level
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()