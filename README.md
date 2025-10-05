# Documentation Downloader v1.0

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful, user-friendly web application that intelligently scrapes documentation websites and converts them into PDF or Markdown files. Built with FastAPI and featuring real-time progress tracking, smart crawling, and professional PDF generation.

## ✨ Features

### � Core Functionality
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

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd doc-download
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv .venv
   
   # On macOS/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. **Start the application**:
   ```bash
   python start_app.py
   ```

2. **Open your browser** and go to: `http://localhost:8000`

3. **Enter a documentation URL** (e.g., `https://docs.python.org/3/tutorial/`)

4. **Select output format** (PDF or Markdown)

5. **Watch the real-time progress** and download your file!

## 📋 Requirements

All dependencies are listed in `requirements.txt`:

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

## 🏗️ Project Structure

```
doc-download/
├── main.py              # FastAPI application and WebSocket handling
├── doc_scraper.py       # Core scraping and PDF/Markdown generation
├── config.py            # Configuration settings
├── start_app.py         # Application startup script
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html       # Web interface template
├── static/             # CSS and JavaScript files
├── downloads/          # Generated files (local serving)
├── temp/              # Temporary files (auto-cleaned)
└── README.md          # This file
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

Edit `config.py` to customize:

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
uvicorn main:app --host 0.0.0.0 --port 8080

# Development mode with auto-reload
uvicorn main:app --reload
```

### API Endpoints
- `GET /` - Web interface
- `POST /download` - Start documentation processing
- `GET /download/{filename}` - Download generated files
- `WebSocket /ws/{connection_id}` - Real-time progress updates

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No module named 'reportlab'"
**Solution**: Ensure virtual environment is activated and run `pip install -r requirements.txt`

**Issue**: PDF generation fails
**Solution**: The app will automatically fall back to HTML files that can be printed to PDF

**Issue**: Downloads not appearing
**Solution**: Check both the project's `downloads/` folder and your system's Downloads folder

### Logs
The application provides detailed logging. Check the console output for:
- Scraping progress
- Error messages
- File generation status

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [ReportLab](https://www.reportlab.com/) - PDF generation
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [Markdownify](https://github.com/matthewwithanm/python-markdownify) - HTML to Markdown conversion

## 📈 Version History

### v1.0.0 (2025-10-05)
- ✨ Initial release
- 📄 ReportLab PDF generation
- 🔗 Intelligent documentation crawling
- ⚡ Real-time WebSocket progress tracking
- 🧹 Automatic temporary file cleanup
- 🎯 Smart depth-based scraping (no arbitrary page limits)
- 📁 Automatic file delivery to Downloads folder

---

**Made with ❤️ for the developer community**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and go to: `http://localhost:8000`

3. Enter the documentation URL (e.g., `https://fastapi.tiangolo.com/`)

4. Choose your output format (PDF or Markdown)

5. Set the maximum number of pages to download (optional)

6. Click "Download Documentation" and wait for processing

7. The file will be automatically downloaded to your browser

## Supported Documentation Sites

The scraper works best with:
- Python documentation (docs.python.org)
- FastAPI documentation (fastapi.tiangolo.com)
- React documentation (reactjs.org/docs)
- Vue.js documentation (vuejs.org/guide)
- And many other well-structured documentation sites

## Configuration

### Environment Variables

You can customize the application behavior by setting these environment variables:

- `MAX_PAGES_DEFAULT`: Default maximum pages to scrape (default: 50)
- `OUTPUT_DIR`: Directory to save downloaded files (default: downloads)

### Scraping Settings

In `doc_scraper.py`, you can modify:
- Request timeout
- Delay between requests
- Content selectors for different documentation formats
- URL filtering rules

## API Endpoints

- `GET /`: Main web interface
- `POST /download`: Process documentation and return file
- `GET /status`: Health check endpoint

## File Structure

```
doc-download/
├── main.py              # FastAPI application
├── doc_scraper.py       # Documentation scraping logic
├── requirements.txt     # Python dependencies
├── templates/
│   └── index.html      # Web interface template
├── static/             # Static files (CSS, JS, images)
├── downloads/          # Generated files (auto-created)
└── README.md          # This file
```

## Dependencies

- **FastAPI**: Modern web framework for building APIs
- **BeautifulSoup4**: HTML parsing and content extraction
- **WeasyPrint**: PDF generation from HTML
- **Markdownify**: HTML to Markdown conversion
- **Requests**: HTTP library for web scraping
- **Jinja2**: Template engine for HTML rendering

## Troubleshooting

### Common Issues

1. **PDF Generation Errors**: WeasyPrint requires additional system dependencies:
   - On macOS: `brew install pango`
   - On Ubuntu: `sudo apt-get install libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0`

2. **Permission Errors**: Ensure the application has write permissions for the downloads directory

3. **Timeout Errors**: Some sites may be slow to respond. Increase the timeout in `doc_scraper.py`

4. **No Content Found**: The scraper may not recognize the documentation structure. Check the content selectors in `_extract_main_content()`

### Debugging

Enable debug logging by modifying the logging level in `doc_scraper.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Disclaimer

This tool is for educational and personal use. Please respect robots.txt files and website terms of service when scraping documentation. Be mindful of server resources and implement appropriate delays between requests.