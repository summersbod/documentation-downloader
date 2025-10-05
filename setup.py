#!/usr/bin/env python
"""
Documentation Downloader Setup
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

# Read requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="documentation-downloader",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A FastAPI web application for downloading and converting documentation to PDF or Markdown",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/documentation-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "static/*"],
    },
    entry_points={
        "console_scripts": [
            "doc-downloader=start_app:main",
        ],
    },
    keywords="documentation pdf markdown scraping fastapi web converter",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/documentation-downloader/issues",
        "Source": "https://github.com/yourusername/documentation-downloader",
        "Documentation": "https://github.com/yourusername/documentation-downloader#readme",
    },
)