"""
Simple test script for the Documentation Downloader
"""

import asyncio
import os
import sys
from doc_scraper import DocumentationScraper

async def test_scraper():
    """Test the documentation scraper with a simple page"""
    
    print("Testing Documentation Scraper...")
    
    # Test with a simple documentation site
    test_url = "https://httpbin.org/html"  # Simple HTML page for testing
    
    try:
        scraper = DocumentationScraper(test_url)
        
        # Scrape with minimal pages for testing
        print(f"Scraping: {test_url}")
        pages = await scraper.scrape_documentation(max_depth=1, timeout_minutes=1)
        
        if not pages:
            print("❌ No pages found")
            return False
        
        print(f"✅ Successfully scraped {len(pages)} page(s)")
        print(f"   Title: {pages[0]['title']}")
        print(f"   Content length: {len(pages[0]['content'])} characters")
        
        # Test PDF generation (HTML file)
        pdf_path = "test_output.pdf"
        result_path = await scraper.generate_pdf(pages, pdf_path)
        
        if os.path.exists(result_path):
            print(f"✅ PDF (HTML) generated: {result_path}")
        else:
            print("❌ PDF generation failed")
            return False
        
        # Test Markdown generation
        md_path = "test_output.md"
        await scraper.generate_markdown(pages, md_path)
        
        if os.path.exists(md_path):
            print(f"✅ Markdown generated: {md_path}")
        else:
            print("❌ Markdown generation failed")
            return False
        
        # Cleanup test files
        for file_path in [result_path, md_path]:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🧹 Cleaned up: {file_path}")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_imports():
    """Test that all required imports work"""
    
    print("Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI")
        
        import requests
        print("✅ Requests")
        
        import bs4
        print("✅ BeautifulSoup4")
        
        import markdownify
        print("✅ Markdownify")
        
        import aiofiles
        print("✅ Aiofiles")
        
        import jinja2
        print("✅ Jinja2")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

async def main():
    """Main test function"""
    
    print("=" * 50)
    print("Documentation Downloader - Test Suite")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        sys.exit(1)
    
    print("\n" + "=" * 30)
    
    # Test scraper functionality
    if not await test_scraper():
        print("\n❌ Scraper tests failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("The application is ready to use.")
    print("Run 'python start_app.py' to start the web server.")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())