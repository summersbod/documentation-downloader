# Documentation Downloader v1.0

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful, user-friendly web application that intelligently scrapes documentation websites and converts them into PDF or Markdown files. Built with FastAPI and featuring real-time progress tracking, smart crawling, and professional PDF generation.

## ✨ Features

### 🎯 Core Functionality
- **📄 PDF Generation**: Creates professional PDFs using ReportLab with proper formatting
- **📝 Markdown Export**: Generates clean, structured Markdown files
- **🔗 Intelligent Crawling**: Automatically discovers and follows documentation links up to 3 levels deep
- **⏱️ Real-time Progress**: WebSocket-powered progress tracking with 7 detailed steps
- **🛑 Cancellation Support**: Stop long-running processes anytime

### 🖥️ User Experience
- **🌐 Modern Web Interface**: Clean, responsive design that works on all devices
- **📊 Live Progress Updates**: See exactly what's happening during processing
- **📁 Automatic Downloads**: Files saved directly to your Downloads folder
- **🚀 No Dependencies**: Pure Python solution with no external system requirements

### 🔧 Technical Excellence
- **⚡ FastAPI Backend**: High-performance async Python web framework
- **🧹 Smart Cleanup**: Automatic temporary file management
- **🛡️ Error Handling**: Robust error recovery and user feedback
- **📈 Scalable Architecture**: Clean, modular code structure

## 🏗️ Project Structure

```
documentation-downloader/
├── 📄 README.md              # This file
├── 📄 LICENSE                # MIT License
├── 📄 .gitignore             # Git ignore rules
├── 🚀 app.py                 # Main entry point
├── 🚀 start_app.py           # Alternative startup script
│
├── 📁 src/                   # Source code
│   ├── 📁 core/              # Core functionality
│   │   ├── config.py         # Configuration settings
│   │   ├── version.py        # Version information
│   │   └── doc_scraper.py    # Documentation scraping logic
│   │
│   └── 📁 web/               # Web interface
│       ├── main.py           # FastAPI application
│       ├── templates/        # HTML templates
│       └── static/           # CSS/JS assets
│
├── 📁 setup/                 # Package configuration
│   ├── README.md            # Setup documentation
│   ├── requirements.txt     # Dependencies
│   ├── setup.py             # Package distribution
│   └── pyproject.toml       # Modern packaging config
│
├── 📁 tests/                 # Test suite
│   ├── test_app.py          # Basic tests
│   ├── test_enhanced.py     # Enhanced tests
│   └── demo.py              # Demo/example usage
│
├── 📁 docs/                  # Documentation
│   ├── README.md            # Documentation index
│   ├── QUICK_START.md       # Quick start guide
│   ├── PROJECT_STRUCTURE.md # Project organization guide
│   ├── CONTRIBUTING.md      # Contributor guide
│   ├── CHANGELOG.md         # Version history
│   ├── ENHANCEMENTS.md      # Enhancement documentation
│   └── FIXES.md             # Bug fix documentation
│
├── 📁 scripts/               # Utility scripts
│   ├── setup_dev.sh         # Development setup
│   └── prepare_git.sh       # Git preparation
│
├── 📁 downloads/             # Generated files (local)
├── 📁 temp/                  # Temporary files (auto-cleaned)
└── 📁 .venv/                 # Virtual environment (created by setup)
```
├── 📁 downloads/             # Generated files (local)
├── 📁 temp/                  # Temporary files (auto-cleaned)
└── 📁 .venv/                 # Virtual environment (created by setup)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/summersbod/documentation-downloader.git
   cd documentation-downloader
   ```

2. **Quick setup** (automated):
   ```bash
   chmod +x scripts/setup_dev.sh
   ./scripts/setup_dev.sh
   ```

3. **Manual setup** (alternative):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r setup/requirements.txt
   ```

### Usage

**Option 1 - Main entry point:**
```bash
python app.py
```

**Option 2 - Startup script:**
```bash
python start_app.py
```

Then:
1. **Open your browser** and go to: `http://localhost:8000`
2. **Enter a documentation URL** (e.g., `https://docs.python.org/3/tutorial/`)
3. **Select output format** (PDF or Markdown)
4. **Watch the real-time progress** and download your file!

## 📋 Requirements

All dependencies are listed in `setup/requirements.txt`:

```
fastapi>=0.104.1
uvicorn>=0.24.0
jinja2>=3.1.2
python-multipart>=0.0.6
aiofiles>=24.1.0
beautifulsoup4>=4.12.2
markdownify>=0.11.6
python-slugify>=8.0.1
reportlab>=4.0.7
requests>=2.31.0
websockets>=12.0
```

## 🎯 Supported Sites

The application works with most documentation websites that have:
- Standard HTML structure
- Logical link hierarchy
- Accessible content (no heavy JavaScript requirements)

**Tested successfully with**:
- Python documentation
- FastAPI documentation
- VS Code documentation
- GitHub documentation
- Many other standard documentation sites

## ⚙️ Configuration

Edit `src/core/config.py` to customize:

```python
# Scraping behavior
MAX_DEPTH = 3           # Maximum link depth to follow
TIMEOUT_MINUTES = 10    # Maximum scraping time

# Output directories
OUTPUT_DIR = "downloads"                    # Local files
USER_DOWNLOADS_DIR = "~/Downloads"          # User's Downloads folder
TEMP_DIR = "temp"                          # Temporary files
```

## 🔧 Advanced Usage

### Command Line Options
```bash
# Custom host and port
uvicorn src.web.main:app --host 0.0.0.0 --port 8080

# Development mode with auto-reload
uvicorn src.web.main:app --reload
```

### API Endpoints
- `GET /` - Web interface
- `POST /download` - Start documentation processing
- `GET /download/{filename}` - Download generated files
- `WebSocket /ws/{connection_id}` - Real-time progress updates

## 🧪 Testing

Run the test suite:

```bash
# Basic tests
python tests/test_app.py

# Enhanced tests
python tests/test_enhanced.py

# Demo/example usage
python tests/demo.py
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: Import errors or module not found
**Solution**: Ensure you're running from the project root and the virtual environment is activated

**Issue**: "No module named 'reportlab'"
**Solution**: Run `pip install -r setup/requirements.txt` in your activated virtual environment

**Issue**: PDF generation fails
**Solution**: The app will automatically fall back to HTML files that can be printed to PDF

### Logs
The application provides detailed logging. Check the console output for:
- Scraping progress
- Error messages
- File generation status

## 📚 Documentation

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running quickly
- **[IDE Configuration Guide](docs/IDE_CONFIGURATION.md)** - VS Code and other IDE setup
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Understanding the codebase organization
- **[Contributing Guide](docs/CONTRIBUTING.md)** - How to contribute to the project
- **[Changelog](docs/CHANGELOG.md)** - Version history and changes
- **[Development Setup](scripts/setup_dev.sh)** - Automated development environment setup

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details on:
- Setting up the development environment
- Code style and standards
- Testing procedures
- Submitting pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Markdownify](https://github.com/matthewwithanm/python-markdownify) - HTML to Markdown conversion

## 📈 Version History

### v1.0.0 (2025-10-05)
- ✨ Initial release with modular architecture
- 📄 ReportLab PDF generation
- 🔗 Intelligent documentation crawling
- ⚡ Real-time WebSocket progress tracking
- 🧹 Automatic temporary file cleanup
- 🎯 Smart depth-based scraping
- 📁 Organized project structure
- 📚 Comprehensive documentation

---

**Made with ❤️ for the developer community**