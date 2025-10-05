#!/bin/bash
# Git repository preparation script for Documentation Downloader v1.0

echo "📦 Preparing Documentation Downloader v1.0 for Git repository..."

# Initialize Git repository if not already done
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files to Git
echo "📁 Adding files to Git..."
git add .

# Check Git status
echo "📊 Git status:"
git status --short

# Create initial commit
echo ""
echo "💾 Creating initial commit..."
read -p "Enter commit message (default: 'Initial release v1.0.0'): " commit_message
commit_message=${commit_message:-"Initial release v1.0.0

✨ Features:
- FastAPI web application with modern interface
- ReportLab PDF generation (pure Python solution)
- Markdown export functionality
- Real-time WebSocket progress tracking
- Intelligent documentation scraping with depth-based crawling
- Automatic temporary file cleanup
- Cross-platform compatibility
- No external system dependencies

🔧 Technical:
- Python 3.8+ support
- Async/await architecture
- Modular, maintainable codebase
- Comprehensive error handling
- Professional documentation and setup"}

git commit -m "$commit_message"

echo ""
echo "✅ Git repository prepared successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Create a repository on GitHub/GitLab"
echo "2. Add the remote origin:"
echo "   git remote add origin https://github.com/yourusername/documentation-downloader.git"
echo ""
echo "3. Push to remote repository:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Create a release tag:"
echo "   git tag -a v1.0.0 -m 'Version 1.0.0 - Initial Release'"
echo "   git push origin v1.0.0"
echo ""
echo "🎉 Documentation Downloader v1.0 is ready for release!"