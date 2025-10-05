# Setup Configuration

This directory contains all files related to project setup, installation, and packaging.

## Files

### Package Configuration
- **`setup.py`** - Traditional Python package setup script (setuptools)
- **`pyproject.toml`** - Modern Python project configuration (PEP 517/518)
- **`requirements.txt`** - Python dependencies list

### Installation Commands

#### Install from requirements.txt
```bash
pip install -r setup/requirements.txt
```

#### Install in development mode
```bash
pip install -e .
```

#### Build the package
```bash
cd setup/
python -m build
```

#### Install with pip (using pyproject.toml)
```bash
pip install .
```

## Package Structure

The package follows the `src` layout:
- Source code in `src/core/` and `src/web/`
- Tests in `tests/`
- Documentation in `docs/`
- Scripts in `scripts/`

## Dependencies

Core dependencies:
- **FastAPI** - Web framework
- **ReportLab** - PDF generation
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **Aiofiles** - Async file operations

See `requirements.txt` for complete list with version constraints.

## Development Setup

For development environment setup, see the scripts in `scripts/` folder:
- `scripts/setup_dev.sh` - Development environment setup
- `scripts/prepare_git.sh` - Git repository preparation