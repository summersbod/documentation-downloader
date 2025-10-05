"""
Documentation Downloader - Core Package
"""

# Only import version at the package level to avoid dependency issues
try:
    from .core.version import __version__
except ImportError:
    __version__ = "1.0.0"  # Fallback version

__all__ = ['__version__']