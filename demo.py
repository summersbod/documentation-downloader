#!/usr/bin/env python3
"""
Demo script showing how to use the DocumentationScraper programmatically
"""

import asyncio
import sys
from doc_scraper import DocumentationScraper

async def demo_scraping():
    """Demo the documentation scraping functionality"""
    
    print("🚀 Documentation Scraper Demo")
    print("=" * 50)
    
    # Example URLs to try
    example_urls = [
        "https://httpbin.org/html",  # Simple test page
        "https://httpbin.org/",      # API documentation
    ]
    
    print("Available example URLs:")
    for i, url in enumerate(example_urls, 1):
        print(f"  {i}. {url}")
    
    print(f"\nOr enter a custom URL (or press Enter for default: {example_urls[0]})")
    
    # Get user input
    choice = input("Enter choice (1-2) or URL: ").strip()
    
    if choice == "1":
        url = example_urls[0]
    elif choice == "2":
        url = example_urls[1]
    elif choice == "":
        url = example_urls[0]
    elif choice.startswith("http"):
        url = choice
    else:
        print("Invalid choice, using default.")
        url = example_urls[0]
    
    print(f"\n📄 Scraping: {url}")
    print("-" * 50)
    
    try:
        # Initialize scraper
        scraper = DocumentationScraper(url)
        
        # Scrape documentation (limit to 3 pages for demo)
        pages = await scraper.scrape_documentation(max_depth=2, timeout_minutes=2)
        
        if not pages:
            print("❌ No pages found or unable to scrape")
            return
        
        print(f"✅ Successfully scraped {len(pages)} page(s)")
        print("\nPage summaries:")
        for i, page in enumerate(pages, 1):
            print(f"  {i}. {page['title'][:60]}{'...' if len(page['title']) > 60 else ''}")
            print(f"     URL: {page['url']}")
            print(f"     Content: {len(page['content'])} characters")
        
        # Ask user what format they want
        print(f"\n📁 Choose output format:")
        print("  1. HTML (optimized for PDF conversion)")
        print("  2. Markdown")
        print("  3. Both")
        
        format_choice = input("Enter choice (1-3, default: 3): ").strip() or "3"
        
        timestamp = asyncio.get_event_loop().time()
        base_name = f"demo_output_{int(timestamp)}"
        
        if format_choice in ["1", "3"]:
            # Generate HTML
            html_path = f"{base_name}.html"
            result_path = await scraper.generate_pdf(pages, f"{base_name}.pdf")
            print(f"✅ HTML file created: {result_path}")
            print(f"   Open this file in a browser and print to PDF (Cmd/Ctrl + P)")
        
        if format_choice in ["2", "3"]:
            # Generate Markdown
            md_path = f"{base_name}.md"
            await scraper.generate_markdown(pages, md_path)
            print(f"✅ Markdown file created: {md_path}")
        
        print(f"\n🎉 Demo completed successfully!")
        print(f"Files are saved in the current directory.")
        
    except Exception as e:
        print(f"❌ Error during scraping: {str(e)}")
        print(f"Please check the URL and try again.")

def show_usage():
    """Show usage instructions"""
    print("Documentation Scraper - Demo Mode")
    print("=" * 40)
    print("\nThis demo shows how to use the scraper programmatically.")
    print("For the web interface, run: python start_app.py")
    print("\nThe scraper can handle:")
    print("• Documentation websites")
    print("• API reference pages") 
    print("• Technical blogs")
    print("• Knowledge bases")
    print("\nOutput formats:")
    print("• HTML (optimized for PDF conversion)")
    print("• Markdown")
    print("")

async def main():
    """Main demo function"""
    show_usage()
    
    try:
        await demo_scraping()
    except KeyboardInterrupt:
        print("\n\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main())