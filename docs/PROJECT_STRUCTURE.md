# Project Structure

This document describes the organized structure of the Documentation Downloader application.

## Directory Layout

```
doc-download/
├── app.py                  # Main entry point
├── start_app.py           # Alternative entry point
├── requirements.txt       # Python dependencies
├── setup.py              # Package configuration
├── README.md              # Project documentation
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
│
├── src/                   # Source code
│   ├── core/             # Core business logic
│   │   ├── __init__.py
│   │   ├── config.py     # Configuration settings
│   │   ├── version.py    # Version information
│   │   └── doc_scraper.py # Documentation scraping engine
│   │
│   └── web/              # Web interface
│       ├── __init__.py
│       ├── main.py       # FastAPI application
│       ├── templates/    # Jinja2 templates
│       │   └── index.html
│       └── static/       # CSS/JS static files
│           └── style.css
│
├── tests/                 # Test files
│   ├── __init__.py
│   ├── test_app.py       # Application tests
│   ├── test_enhanced.py  # Enhanced feature tests
│   └── demo.py           # Demo script
│
├── docs/                 # Documentation
│   ├── CHANGELOG.md      # Version history
│   ├── CONTRIBUTING.md   # Contribution guidelines
│   ├── ENHANCEMENTS.md   # Enhancement documentation
│   ├── FIXES.md          # Bug fix documentation
│   ├── PRE_RELEASE_CHECKLIST.md
│   └── QUICK_START.md    # Quick start guide
│
├── scripts/              # Utility scripts
│   ├── setup_dev.sh     # Development setup
│   └── prepare_git.sh   # Git preparation
│
├── downloads/            # User downloads directory
├── temp/                 # Temporary files
└── .venv/               # Virtual environment
```

## Running the Application

### Method 1: Main Entry Point
```bash
python app.py
```

### Method 2: Alternative Entry Point
```bash
python start_app.py
```

Both methods will start the FastAPI server on http://localhost:8000

## Benefits of This Structure

1. **Separation of Concerns**: Core logic separated from web interface
2. **Easy Testing**: All tests organized in dedicated directory
3. **Clear Documentation**: All docs in one place
4. **Utility Scripts**: Development and deployment scripts organized
5. **Scalability**: Easy to add new modules in appropriate directories
6. **Professional Layout**: Follows Python packaging best practices

## Module Organization

- **src/core/**: Contains the core business logic that could be reused
- **src/web/**: Contains web-specific code (FastAPI, templates, static files)
- **tests/**: All test files for different components
- **docs/**: User and developer documentation
- **scripts/**: Development and deployment automation

This structure makes the codebase more maintainable and professional.