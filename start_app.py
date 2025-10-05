#!/usr/bin/env python3
"""
Startup script for Documentation Downloader
Handles dependency checking and provides helpful error messages
"""

import sys
import subprocess
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_reportlab():
    """Check if ReportLab can be imported successfully"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        return True, "ReportLab available - generating actual PDF files"
    except ImportError:
        return False, "ReportLab not available - using HTML files for PDF generation"

def install_system_dependencies_help():
    """Provide help for PDF generation when ReportLab is not available"""
    print("\n" + "="*60)
    print("PDF GENERATION INFORMATION")
    print("="*60)
    print("\nThis application generates HTML files optimized for PDF conversion.")
    print("To convert to PDF, follow these simple steps:\n")
    
    print("1. Download the HTML file")
    print("2. Open it in any web browser")
    print("3. Press Ctrl+P (Windows/Linux) or Cmd+P (Mac)")
    print("4. Select 'Save as PDF' as the destination")
    print("5. Click 'Save'\n")
    
    print("The HTML files are specially formatted for printing and include:")
    print("• Professional styling optimized for PDF")
    print("• Automatic page breaks")
    print("• Table of contents")
    print("• Print-friendly formatting")
    print("="*60 + "\n")

def main():
    """Main startup function"""
    print("Starting Documentation Downloader...")
    
    # Check ReportLab availability
    reportlab_available, message = check_reportlab()
    
    if not reportlab_available:
        print(f"ℹ️  {message}")
        install_system_dependencies_help()
    else:
        print(f"✅ {message}")
        print("\n" + "="*60)
        print("PDF GENERATION READY")
        print("="*60)
        print("\n✓ ReportLab is installed and ready")
        print("✓ Real PDF files will be generated")
        print("✓ No system dependencies required")
        print("✓ Professional formatting included")
        print("="*60 + "\n")
    
    # Start the FastAPI application
    print("\nStarting FastAPI server...")
    print("Access the application at: http://localhost:8000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        import uvicorn
        from web.main import app
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()