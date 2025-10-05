"""
Documentation Downloader - Core Functionality Package
"""

from .version import __version__

# Lazy imports to avoid dependency issues during startup
def get_documentation_scraper():
    """Lazy import of DocumentationScraper to avoid early dependency loading"""
    from .doc_scraper import DocumentationScraper
    return DocumentationScraper

__all__ = ['__version__', 'get_documentation_scraper']