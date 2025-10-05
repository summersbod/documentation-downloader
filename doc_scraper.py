import requests
from bs4 import BeautifulSoup
import asyncio
import aiofiles
import os
import tempfile
from urllib.parse import urljoin, urlparse, parse_qs
from markdownify import markdownify as md
# Import for PDF generation
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("ReportLab not available. PDF generation will create HTML files instead.")
from slugify import slugify
import re
from typing import List, Dict, Optional
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import config settings
try:
    from config import TEMP_DIR
except ImportError:
    TEMP_DIR = "temp"  # Fallback if config import fails

class DocumentationScraper:
    def __init__(self, base_url: str, progress_tracker=None):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls = set()
        self.pages = []
        self.progress_tracker = progress_tracker
        
        # Clean up old temp files on initialization
        self._cleanup_old_temp_files()
    
    def _cleanup_old_temp_files(self):
        """Clean up old temporary HTML files"""
        try:
            if os.path.exists(TEMP_DIR):
                for filename in os.listdir(TEMP_DIR):
                    if filename.startswith('temp_doc_') and filename.endswith('.html'):
                        file_path = os.path.join(TEMP_DIR, filename)
                        try:
                            # Remove files older than 1 hour
                            file_age = datetime.now().timestamp() - os.path.getmtime(file_path)
                            if file_age > 3600:  # 1 hour in seconds
                                os.remove(file_path)
                                logger.info(f"Cleaned up old temp file: {filename}")
                        except Exception as e:
                            logger.warning(f"Could not clean up {filename}: {e}")
        except Exception as e:
            logger.warning(f"Error during temp file cleanup: {e}")

    async def scrape_documentation(self, max_depth: int = 3, timeout_minutes: int = 10) -> List[Dict]:
        """Scrape documentation pages starting from the base URL
        
        Args:
            max_depth: Maximum link depth to follow (default: 3 levels deep)
            timeout_minutes: Maximum time to spend scraping (default: 10 minutes)
        """
        
        logger.info(f"Starting to scrape documentation from {self.base_url}")
        
        import time
        start_time = time.time()
        timeout_seconds = timeout_minutes * 60
        
        # Start with the base URL at depth 0
        urls_to_visit = [(self.base_url, 0)]
        
        while urls_to_visit:
            # Check timeout
            if time.time() - start_time > timeout_seconds:
                logger.info(f"Timeout reached after {timeout_minutes} minutes. Scraped {len(self.pages)} pages.")
                break
                
            current_url, depth = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls or depth > max_depth:
                continue
            
            # Send progress update
            if self.progress_tracker:
                await self.progress_tracker.send_progress(
                    3, 7, 
                    f"📖 Extracting documentation ({len(self.pages)} pages found)",
                    f"Processing: {current_url[:80]}..."
                )
                
            try:
                page_data = await self._scrape_page(current_url)
                if page_data:
                    self.pages.append(page_data)
                    
                    # Find more documentation links on this page (only if we haven't reached max depth)
                    if depth < max_depth:
                        new_urls = self._extract_documentation_links(page_data['soup'], current_url)
                        
                        # Add new URLs to visit with incremented depth
                        for url in new_urls:
                            if url not in self.visited_urls and self._is_documentation_url(url):
                                urls_to_visit.append((url, depth + 1))
                
                self.visited_urls.add(current_url)
                
                # Small delay to be respectful to the server
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error scraping {current_url}: {str(e)}")
                continue
        
        logger.info(f"Scraped {len(self.pages)} pages")
        return self.pages

    async def _scrape_page(self, url: str) -> Optional[Dict]:
        """Scrape a single page and extract content"""
        
        try:
            logger.info(f"Scraping: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup, url)
            
            # Extract main content
            content = self._extract_main_content(soup)
            
            if not content.strip():
                logger.warning(f"No content extracted from {url}")
                return None
            
            return {
                'url': url,
                'title': title,
                'content': content,
                'soup': soup
            }
            
        except Exception as e:
            logger.error(f"Failed to scrape {url}: {str(e)}")
            return None

    def _extract_title(self, soup: BeautifulSoup, url: str) -> str:
        """Extract page title"""
        
        # Try different title selectors
        title_selectors = [
            'h1',
            'title',
            '.page-title',
            '.doc-title',
            '.content-title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text().strip()
                if title:
                    return title
        
        # Fallback to URL-based title
        return urlparse(url).path.split('/')[-1] or 'Documentation Page'

    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from the page"""
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', '.sidebar', '.navigation']):
            element.decompose()
        
        # Try to find main content area
        content_selectors = [
            'main',
            '.content',
            '.main-content',
            '.doc-content',
            '.documentation',
            '.article',
            'article',
            '.page-content',
            '.markdown-body'
        ]
        
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                return content_element.get_text().strip()
        
        # Fallback: get body content
        body = soup.find('body')
        if body:
            return body.get_text().strip()
        
        return soup.get_text().strip()

    def _extract_documentation_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extract links that likely point to documentation pages"""
        
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Convert relative URLs to absolute
            full_url = urljoin(current_url, href)
            
            # Filter links
            if self._is_documentation_url(full_url):
                links.append(full_url)
        
        return list(set(links))  # Remove duplicates

    def _is_documentation_url(self, url: str) -> bool:
        """Check if URL is likely a documentation page"""
        
        parsed_url = urlparse(url)
        
        # Must be from same domain
        if parsed_url.netloc != self.domain:
            return False
        
        # Skip certain file types
        path = parsed_url.path.lower()
        skip_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.pdf', '.zip']
        if any(path.endswith(ext) for ext in skip_extensions):
            return False
        
        # Skip fragments and queries that suggest non-content pages
        if '#' in url or '?' in url:
            return False
        
        # Skip common non-documentation paths
        skip_paths = ['/login', '/register', '/search', '/api/', '/admin']
        if any(skip_path in path for skip_path in skip_paths):
            return False
        
        return True

    async def generate_pdf(self, pages: List[Dict], output_path: str, progress_tracker=None):
        """Generate PDF from scraped pages using ReportLab"""
        
        logger.info(f"Generating PDF with {len(pages)} pages")
        
        # Create temporary HTML file for intermediate processing
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_html_filename = f"temp_doc_{timestamp}.html"
        temp_html_path = os.path.join(TEMP_DIR, temp_html_filename)
        
        # Ensure temp directory exists
        os.makedirs(TEMP_DIR, exist_ok=True)
        
        try:
            if REPORTLAB_AVAILABLE:
                try:
                    # Create PDF document directly with ReportLab
                    doc = SimpleDocTemplate(output_path, pagesize=A4)
                    story = []
                    
                    # Get styles
                    styles = getSampleStyleSheet()
                    title_style = styles['Title']
                    heading_style = styles['Heading1']
                    normal_style = styles['Normal']
                    
                    # Add title page
                    story.append(Paragraph("📚 Documentation", title_style))
                    story.append(Spacer(1, 0.5*inch))
                    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
                    story.append(Paragraph(f"Total Pages: {len(pages)}", normal_style))
                    story.append(PageBreak())
                    
                    # Add content
                    for i, page in enumerate(pages):
                        if progress_tracker and i % 5 == 0:  # Update progress every 5 pages
                            progress_percent = (i / len(pages)) * 0.8 + 0.1  # 10-90% of step 5
                            await progress_tracker.send_progress(5, 7, "📄 Creating PDF file", 
                                                               f"Processing page {i+1}/{len(pages)}: {page['title'][:50]}...")
                        
                        # Add page title
                        story.append(Paragraph(page['title'], heading_style))
                        story.append(Spacer(1, 0.2*inch))
                        
                        # Add page URL
                        story.append(Paragraph(f"<i>Source: {page['url']}</i>", normal_style))
                        story.append(Spacer(1, 0.2*inch))
                        
                        # Add content (clean and format)
                        content = self._clean_text_for_pdf(page['content'])
                        
                        # Split content into paragraphs
                        paragraphs = content.split('\n\n')
                        for para in paragraphs:
                            if para.strip():
                                try:
                                    story.append(Paragraph(para.strip(), normal_style))
                                    story.append(Spacer(1, 0.1*inch))
                                except Exception as e:
                                    # If paragraph fails, add as plain text
                                    logger.warning(f"Failed to add paragraph: {str(e)[:100]}")
                                    continue
                        
                        # Add page break between pages
                        if i < len(pages) - 1:
                            story.append(PageBreak())
                    
                    # Build PDF
                    doc.build(story)
                    logger.info(f"PDF saved to {output_path}")
                    
                    if progress_tracker:
                        await progress_tracker.send_progress(6, 7, "✅ PDF generation complete", f"PDF saved: {os.path.basename(output_path)}")
                    
                    return output_path
                    
                except Exception as e:
                    logger.error(f"Error generating PDF with ReportLab: {str(e)}")
                    # Create temporary HTML file for fallback
                    html_content = self._create_printable_html_document(pages)
                    async with aiofiles.open(temp_html_path, 'w', encoding='utf-8') as f:
                        await f.write(html_content)
                    logger.info(f"Created temporary HTML file: {temp_html_path}")
                    # Note: We'll keep the temp HTML file as fallback
                    pass
            
            # Fallback: Save as HTML file with PDF-like formatting
            html_content = self._create_printable_html_document(pages)
            html_output_path = output_path.replace('.pdf', '_printable.html')
            async with aiofiles.open(html_output_path, 'w', encoding='utf-8') as f:
                await f.write(html_content)
            
            logger.info(f"Printable HTML file saved to {html_output_path}")
            logger.info("To convert to PDF: Open the HTML file in your browser and print to PDF (Cmd/Ctrl + P)")
            
            if progress_tracker:
                await progress_tracker.send_progress(6, 7, "✅ HTML file ready for PDF conversion", 
                                                    f"Open {os.path.basename(html_output_path)} in browser and print to PDF")
            
            return html_output_path
            
        finally:
            # Clean up temporary HTML file if it exists
            if os.path.exists(temp_html_path):
                try:
                    os.remove(temp_html_path)
                    logger.info(f"Cleaned up temporary HTML file: {temp_html_filename}")
                except Exception as e:
                    logger.warning(f"Could not remove temporary HTML file: {e}")

    def _clean_text_for_pdf(self, text: str) -> str:
        """Clean text for PDF generation"""
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        # Escape XML characters for ReportLab
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        # Ensure proper line endings
        text = text.strip()
        
        return text

    async def generate_markdown(self, pages: List[Dict], output_path: str):
        """Generate Markdown file from scraped pages"""
        
        logger.info(f"Generating Markdown with {len(pages)} pages")
        
        markdown_content = self._create_markdown_document(pages)
        
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
            await f.write(markdown_content)
        
        logger.info(f"Markdown saved to {output_path}")

    def _create_html_document(self, pages: List[Dict]) -> str:
        """Create a complete HTML document from pages"""
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="utf-8">',
            '<title>Documentation</title>',
            '<style>',
            'body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }',
            'h1, h2, h3 { color: #333; }',
            '.page-break { page-break-before: always; }',
            '.page-title { border-bottom: 2px solid #333; padding-bottom: 10px; }',
            'pre { background: #f4f4f4; padding: 10px; overflow-x: auto; }',
            'code { background: #f4f4f4; padding: 2px 4px; }',
            '</style>',
            '</head>',
            '<body>'
        ]
        
        for i, page in enumerate(pages):
            if i > 0:
                html_parts.append('<div class="page-break"></div>')
            
            html_parts.append(f'<h1 class="page-title">{page["title"]}</h1>')
            
            # Convert content to HTML (basic formatting)
            content_html = self._text_to_html(page['content'])
            html_parts.append(content_html)
        
        html_parts.extend(['</body>', '</html>'])
        
        return '\n'.join(html_parts)

    def _create_printable_html_document(self, pages: List[Dict]) -> str:
        """Create a complete HTML document optimized for printing/PDF conversion"""
        
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            '<meta charset="utf-8">',
            '<title>Documentation - Ready for PDF</title>',
            '<style>',
            '@media print {',
            '  body { margin: 0; }',
            '  .page-break { page-break-before: always; }',
            '  .no-print { display: none; }',
            '}',
            'body { font-family: "Times New Roman", Times, serif; line-height: 1.6; margin: 20px; color: #333; }',
            'h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; font-size: 2em; }',
            'h2 { color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; margin-top: 30px; }',
            'h3 { color: #34495e; margin-top: 25px; }',
            '.page-break { page-break-before: always; margin-top: 50px; }',
            '.page-title { border-bottom: 2px solid #3498db; padding-bottom: 15px; margin-bottom: 20px; }',
            '.page-url { font-size: 0.9em; color: #7f8c8d; margin-bottom: 20px; font-style: italic; }',
            'pre { background: #f8f9fa; padding: 15px; border-left: 4px solid #3498db; overflow-x: auto; margin: 15px 0; }',
            'code { background: #f1f2f6; padding: 3px 6px; border-radius: 3px; font-family: "Courier New", monospace; }',
            'p { margin: 10px 0; text-align: justify; }',
            '.toc { background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 30px; }',
            '.toc h2 { margin-top: 0; }',
            '.toc ul { list-style-type: none; padding-left: 0; }',
            '.toc li { margin: 5px 0; }',
            '.toc a { text-decoration: none; color: #3498db; }',
            '.print-instruction { background: #e8f4f8; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #3498db; }',
            '</style>',
            '</head>',
            '<body>'
        ]
        
        # Add print instructions
        html_parts.append('''
        <div class="print-instruction no-print">
            <h3>📄 How to convert this to PDF:</h3>
            <ol>
                <li>Press <strong>Ctrl+P</strong> (Windows/Linux) or <strong>Cmd+P</strong> (Mac)</li>
                <li>Select "Save as PDF" as the destination</li>
                <li>Choose "More settings" and select "Paper size: A4" for best results</li>
                <li>Click "Save" and choose your download location</li>
            </ol>
            <p><em>This instruction box will not appear in the printed version.</em></p>
        </div>
        ''')
        
        # Add title page
        html_parts.append('<div class="title-page">')
        html_parts.append('<h1 style="text-align: center; margin-top: 100px; font-size: 3em;">📚 Documentation</h1>')
        html_parts.append(f'<p style="text-align: center; font-size: 1.2em; margin-top: 30px;">Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>')
        html_parts.append(f'<p style="text-align: center; margin-top: 50px;"><strong>Total Pages:</strong> {len(pages)}</p>')
        html_parts.append('</div>')
        
        # Add table of contents
        html_parts.append('<div class="page-break"></div>')
        html_parts.append('<div class="toc">')
        html_parts.append('<h2>📋 Table of Contents</h2>')
        html_parts.append('<ul>')
        for i, page in enumerate(pages, 1):
            safe_title = page["title"][:80] + "..." if len(page["title"]) > 80 else page["title"]
            html_parts.append(f'<li>{i}. <a href="#page-{i}">{safe_title}</a></li>')
        html_parts.append('</ul>')
        html_parts.append('</div>')
        
        # Add content pages
        for i, page in enumerate(pages, 1):
            html_parts.append('<div class="page-break"></div>')
            html_parts.append(f'<div id="page-{i}">')
            html_parts.append(f'<h1 class="page-title">{page["title"]}</h1>')
            html_parts.append(f'<div class="page-url">Source: {page["url"]}</div>')
            
            # Convert content to HTML with better formatting
            content_html = self._text_to_formatted_html(page['content'])
            html_parts.append(content_html)
            html_parts.append('</div>')
        
        html_parts.extend(['</body>', '</html>'])
        
        return '\n'.join(html_parts)

    def _create_markdown_document(self, pages: List[Dict]) -> str:
        """Create a markdown document from pages"""
        
        markdown_parts = [
            '# Documentation',
            '',
            f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '',
            '---',
            ''
        ]
        
        for page in pages:
            markdown_parts.append(f'## {page["title"]}')
            markdown_parts.append('')
            markdown_parts.append(f'**Source:** {page["url"]}')
            markdown_parts.append('')
            
            # Clean and format content
            content = self._clean_text_for_markdown(page['content'])
            markdown_parts.append(content)
            markdown_parts.append('')
            markdown_parts.append('---')
            markdown_parts.append('')
        
        return '\n'.join(markdown_parts)

    def _text_to_html(self, text: str) -> str:
        """Convert plain text to basic HTML with formatting"""
        
        # Escape HTML characters
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Convert newlines to paragraphs
        paragraphs = text.split('\n\n')
        html_paragraphs = [f'<p>{p.replace(chr(10), "<br>")}</p>' for p in paragraphs if p.strip()]
        
        return '\n'.join(html_paragraphs)

    def _text_to_formatted_html(self, text: str) -> str:
        """Convert plain text to well-formatted HTML"""
        
        # Escape HTML characters
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        html_parts = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            # Check if it looks like a heading (short line, potentially all caps or title case)
            if len(paragraph) < 100 and paragraph.isupper():
                html_parts.append(f'<h3>{paragraph}</h3>')
            elif len(paragraph) < 80 and not '.' in paragraph[-10:]:
                # Might be a subheading
                html_parts.append(f'<h4>{paragraph}</h4>')
            else:
                # Regular paragraph
                formatted_paragraph = paragraph.replace('\n', '<br>')
                html_parts.append(f'<p>{formatted_paragraph}</p>')
        
        return '\n'.join(html_parts)

    def _text_to_formatted_html(self, text: str) -> str:
        """Convert plain text to formatted HTML with better structure"""
        
        # Escape HTML characters
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Split into paragraphs
        paragraphs = text.split('\n\n')
        html_parts = []
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
                
            # Check if it looks like a heading (short line, possibly all caps)
            if len(paragraph) < 100 and (paragraph.isupper() or paragraph.count(' ') < 3):
                if len(paragraph) < 50:
                    html_parts.append(f'<h3>{paragraph.strip()}</h3>')
                else:
                    html_parts.append(f'<h4>{paragraph.strip()}</h4>')
            # Check if it looks like a list item
            elif paragraph.strip().startswith(('•', '-', '*', '1.', '2.', '3.')):
                items = paragraph.split('\n')
                html_parts.append('<ul>')
                for item in items:
                    if item.strip():
                        html_parts.append(f'<li>{item.strip()}</li>')
                html_parts.append('</ul>')
            # Regular paragraph
            else:
                # Handle line breaks within paragraph
                formatted_para = paragraph.replace('\n', '<br>')
                html_parts.append(f'<p>{formatted_para}</p>')
        
        return '\n'.join(html_parts)

    def _clean_text_for_markdown(self, text: str) -> str:
        """Clean and format text for markdown"""
        
        # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        # Ensure proper line endings
        text = text.strip()
        
        return text