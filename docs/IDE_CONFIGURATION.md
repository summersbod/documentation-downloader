# IDE Configuration Guide

This document explains how to properly configure your IDE for the Documentation Downloader project.

## VS Code Configuration

The project includes pre-configured VS Code settings in `.vscode/settings.json` that:

### Python Path Resolution
- **Extra Paths**: Adds `./src` to Python analysis paths
- **Auto Search**: Enables automatic path discovery
- **Workspace Analysis**: Analyzes the entire workspace for better imports

### Python Interpreter
- **Default Interpreter**: Points to `./.venv/bin/python`
- **Auto Activation**: Automatically activates the virtual environment in terminals

### Code Quality
- **Type Checking**: Basic type checking enabled
- **Auto Imports**: Intelligent import completions
- **Linting**: Flake8 enabled for code quality
- **Formatting**: Black formatter configured

## Resolving Import Warnings

If you see warnings like `Import "core.version" could not be resolved`, ensure:

1. **VS Code is using the correct Python interpreter**:
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
   - Type "Python: Select Interpreter"
   - Choose the interpreter from `.venv/bin/python`

2. **Pylance is configured correctly**:
   - The project includes `pyproject.toml` with Pylance configuration
   - Extra paths are set to include the `src` directory

3. **Reload VS Code window if needed**:
   - Press `Cmd+Shift+P` / `Ctrl+Shift+P`
   - Type "Developer: Reload Window"

## Project Structure for IDEs

The project uses this structure for import resolution:

```
doc-download/
├── src/                    # Source code (added to Python path)
│   ├── core/              # Core modules
│   │   ├── __init__.py    # Package initialization
│   │   ├── version.py     # Version information
│   │   └── ...
│   └── web/               # Web modules
├── app.py                 # Main entry (adds src to path)
├── .vscode/               # VS Code configuration
├── pyproject.toml         # Python project configuration
└── .env.example           # Environment variables template
```

## Other IDEs

### PyCharm
1. Mark `src` as Sources Root:
   - Right-click on `src` folder
   - Mark Directory as → Sources Root

### Other Editors
- Add `./src` to your Python path
- Set interpreter to `./.venv/bin/python`
- Configure your editor to recognize the project structure

## Troubleshooting

**Import warnings persist?**
1. Check that your IDE is using the virtual environment Python interpreter
2. Verify that `src` is in the Python path configuration
3. Restart your IDE/language server
4. Check that dependencies are installed in the virtual environment

**Type checking issues?**
- The project uses `# type: ignore` comments for dynamic imports
- This is intentional to handle the flexible import structure
- The application includes proper error handling for import failures