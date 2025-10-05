"""
Configuration settings for the Documentation Downloader
"""

import os

# Application settings
APP_TITLE = "Documentation Downloader"
APP_DESCRIPTION = "Download and convert documentation to PDF or Markdown"
APP_VERSION = "1.0.0"

# Server settings
HOST = "0.0.0.0"
PORT = 8000

# Directory settings
OUTPUT_DIR = "downloads"  # Local downloads for web serving
USER_DOWNLOADS_DIR = os.path.expanduser("~/Downloads")  # User's system Downloads folder
TEMP_DIR = "temp"  # Temporary files (HTML before PDF conversion)
TEMPLATE_DIR = "templates"
STATIC_DIR = "static"

# Scraping settings  
MAX_DEPTH = 3  # Maximum link depth to follow
TIMEOUT_MINUTES = 10  # Maximum time to spend scraping
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5  # Delay between requests in seconds

# Content extraction settings
CONTENT_SELECTORS = [
    'main',
    '.content',
    '.main-content',
    '.doc-content',
    '.documentation',
    '.article',
    'article',
    '.page-content',
    '.markdown-body',
    '.rst-content'
]

TITLE_SELECTORS = [
    'h1',
    'title',
    '.page-title',
    '.doc-title',
    '.content-title'
]

# URL filtering settings
SKIP_EXTENSIONS = [
    '.png', '.jpg', '.jpeg', '.gif', '.svg',
    '.css', '.js', '.json',
    '.pdf', '.zip', '.tar.gz',
    '.mp4', '.mp3', '.avi',
    '.exe', '.dmg', '.deb', '.rpm'
]

SKIP_PATHS = [
    '/login', '/register', '/signup', '/signin',
    '/search', '/api/', '/admin',
    '/download', '/downloads',
    '/edit', '/delete'
]

# User agent for web scraping
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)