#!/usr/bin/env python3
"""
Documentation Downloader - Main Entry Point
This is the main entry point for the Documentation Downloader application.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.version import __version__
from start_app import main

if __name__ == "__main__":
    print(f"Documentation Downloader v{__version__}")
    main()