"""
Documentation Downloader - Core Functionality Package
"""

from .config import *
from .version import __version__
from .doc_scraper import DocumentationScraper

__all__ = ['DocumentationScraper', '__version__']