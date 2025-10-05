# Quick Start Guide

## 🚀 Getting Started

### 1. Basic Usage
```bash
# Start the application
python start_app.py

# Or use the production script
python run.py
```

### 2. Access the Web Interface
Open your browser and go to: `http://localhost:8000`

### 3. Download Documentation
1. Enter a documentation URL (e.g., `https://docs.python.org/3/`)
2. Choose output format (PDF/Markdown)
3. Set maximum pages (optional)
4. Click "Download Documentation"

## 📋 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `start_app.py` | Simple startup with helpful messages | `python start_app.py` |
| `run.py` | Production-ready with options | `python run.py --help` |
| `test_app.py` | Test suite | `python test_app.py` |
| `demo.py` | Interactive demo | `python demo.py` |

## 🔧 Command Line Options (run.py)

```bash
python run.py --host 0.0.0.0 --port 8080 --reload
```

Options:
- `--host`: Host to bind to (default: 0.0.0.0)
- `--port`: Port to bind to (default: 8000)
- `--reload`: Enable auto-reload for development
- `--workers`: Number of worker processes
- `--log-level`: Set logging level (debug/info/warning/error)
- `--check`: Check dependencies and exit

## 📄 PDF Generation

Since WeasyPrint requires system dependencies, this app generates HTML files optimized for PDF conversion:

1. Download the HTML file
2. Open in any browser
3. Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (Mac)
4. Select "Save as PDF"
5. Click Save

## 🌐 Supported Sites

Works best with:
- Python documentation
- FastAPI documentation  
- React/Vue documentation
- Well-structured documentation sites

## ⚙️ Configuration

Edit `config.py` to customize:
- Maximum pages
- Request delays
- Content selectors
- Output directories

## 🐛 Troubleshooting

1. **No content found**: Check if the site structure is supported
2. **Slow scraping**: Increase request delay in config
3. **Import errors**: Run `python run.py --check`

## 📚 Examples

### Web Interface
```
URL: https://fastapi.tiangolo.com/
Format: PDF (HTML)
Max Pages: 20
```

### Programmatic Usage
```python
from doc_scraper import DocumentationScraper

scraper = DocumentationScraper("https://docs.python.org/3/")
pages = await scraper.scrape_documentation(max_pages=10)
await scraper.generate_markdown(pages, "python_docs.md")
```