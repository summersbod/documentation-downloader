# Contributing to Documentation Downloader

Thank you for your interest in contributing to Documentation Downloader! This guide will help you get started.

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A code editor (VS Code recommended)

### Development Setup

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/documentation-downloader.git
   cd documentation-downloader
   ```

3. **Run the setup script**:
   ```bash
   chmod +x setup_dev.sh
   ./setup_dev.sh
   ```

4. **Activate the virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

5. **Test the installation**:
   ```bash
   python start_app.py
   ```

## 🏗️ Project Structure

```
doc-download/
├── main.py              # FastAPI application
├── doc_scraper.py       # Core scraping logic
├── config.py            # Configuration settings
├── start_app.py         # Application startup
├── templates/           # HTML templates
├── static/             # CSS/JS files
├── downloads/          # Generated files
├── temp/              # Temporary files
└── tests/             # Test files
```

### Key Components

- **`main.py`**: FastAPI routes, WebSocket handling, background tasks
- **`doc_scraper.py`**: Documentation scraping, PDF/Markdown generation
- **`config.py`**: All configuration settings in one place
- **`templates/index.html`**: Web interface with real-time progress

## 🔧 Making Changes

### Branch Strategy

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test your changes** thoroughly

4. **Commit with descriptive messages**:
   ```bash
   git commit -m "Add: New feature description"
   ```

### Commit Message Format

Use clear, descriptive commit messages:

- `Add:` for new features
- `Fix:` for bug fixes
- `Update:` for improvements to existing features
- `Remove:` for deleted code/features
- `Docs:` for documentation changes

## 🧪 Testing

### Manual Testing

1. **Start the application**:
   ```bash
   python start_app.py
   ```

2. **Test various scenarios**:
   - Different documentation sites
   - PDF and Markdown generation
   - Progress tracking
   - Error handling
   - Cancellation functionality

### Automated Testing

```bash
# Run the test suite
python test_app.py

# Run enhanced tests
python test_enhanced.py
```

### Testing Checklist

- [ ] Application starts without errors
- [ ] Web interface loads correctly
- [ ] Documentation scraping works
- [ ] PDF generation functions
- [ ] Markdown export works
- [ ] Progress updates display
- [ ] Error handling works
- [ ] Files save to correct locations
- [ ] Temporary files are cleaned up

## 📝 Code Style

### Python Code Standards

- **PEP 8** compliance
- **Type hints** where appropriate
- **Docstrings** for all functions and classes
- **Meaningful variable names**
- **Error handling** with try/except blocks

### Example Function:

```python
async def scrape_documentation(self, max_depth: int = 3) -> List[Dict]:
    """Scrape documentation pages starting from the base URL
    
    Args:
        max_depth: Maximum link depth to follow
        
    Returns:
        List of scraped page dictionaries
        
    Raises:
        RequestException: If network request fails
    """
    # Implementation here
```

### Frontend Standards

- **Responsive design** for all screen sizes
- **Accessibility** considerations
- **Progressive enhancement**
- **Clean, semantic HTML**

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected vs actual behavior**
4. **Environment details** (OS, Python version)
5. **Error messages or logs**
6. **Screenshots** if applicable

### Bug Report Template

```markdown
**Bug Description**
A clear description of what the bug is.

**To Reproduce**
1. Go to '...'
2. Click on '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g., macOS 12.0]
- Python: [e.g., 3.9.0]
- Browser: [e.g., Chrome 95.0]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** in detail
3. **Explain the use case** and benefits
4. **Consider implementation complexity**

### Feature Request Template

```markdown
**Feature Description**
A clear description of the feature you'd like to see.

**Problem It Solves**
What problem does this feature address?

**Proposed Solution**
How would you like this feature to work?

**Alternatives Considered**
Any alternative solutions you've thought about.

**Additional Context**
Any other context about the feature request.
```

## 📤 Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** with your changes
5. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots for UI changes

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Manual testing completed
- [ ] Automated tests pass
- [ ] No breaking changes

## Screenshots
(If applicable)

## Related Issues
Fixes #(issue number)
```

## 🎯 Areas for Contribution

We especially welcome contributions in:

- **New documentation site support**
- **PDF formatting improvements**
- **Performance optimizations**
- **UI/UX enhancements**
- **Error handling improvements**
- **Test coverage expansion**
- **Documentation improvements**

## 🤝 Code of Conduct

Please be respectful and inclusive in all interactions. We want this to be a welcoming community for everyone.

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check the README and inline comments

## 🏆 Recognition

Contributors will be recognized in:
- **CHANGELOG.md** for their contributions
- **README.md** in the acknowledgments section
- **GitHub contributors** page

Thank you for contributing to Documentation Downloader! 🚀