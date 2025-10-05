#!/bin/bash
# Development setup script

echo "🚀 Setting up Documentation Downloader for development..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )\d+\.\d+')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Python $required_version or higher is required (found $python_version)"
    exit 1
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📋 Installing dependencies..."
pip install -r setup/requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p downloads temp static templates

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "1. source .venv/bin/activate"
echo "2. python start_app.py"
echo ""
echo "Then open: http://localhost:8000"