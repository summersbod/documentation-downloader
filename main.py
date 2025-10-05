from fastapi import FastAPI, Request, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import aiofiles
import asyncio
import os
import shutil
import json
import uuid
from datetime import datetime
from doc_scraper import DocumentationScraper
from config import OUTPUT_DIR, USER_DOWNLOADS_DIR, TEMP_DIR, TEMPLATE_DIR

app = FastAPI(title="Documentation Downloader", description="Download and convert documentation to PDF or Markdown")

# Setup templates and static files
templates = Jinja2Templates(directory=TEMPLATE_DIR)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(USER_DOWNLOADS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Store active WebSocket connections
active_connections = {}

class ProgressTracker:
    def __init__(self, connection_id: str):
        self.connection_id = connection_id
        self.websocket = active_connections.get(connection_id)
    
    async def send_progress(self, step: int, total_steps: int, message: str, details: str = ""):
        websocket = active_connections.get(self.connection_id)
        if websocket:
            try:
                progress_data = {
                    "type": "progress",
                    "step": step,
                    "total_steps": total_steps,
                    "message": message,
                    "details": details,
                    "progress": round((step / total_steps) * 100, 1)
                }
                await websocket.send_text(json.dumps(progress_data))
                print(f"Progress sent: Step {step}/{total_steps} - {message}")  # Debug log
            except Exception as e:
                print(f"Failed to send progress: {e}")  # Debug log
                pass

@app.websocket("/ws/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, connection_id: str):
    await websocket.accept()
    active_connections[connection_id] = websocket
    try:
        # Keep connection alive
        while True:
            # Wait for messages or send periodic ping
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                # Echo back any received messages
                await websocket.send_text(json.dumps({"type": "ping", "message": "Connection alive"}))
            except asyncio.TimeoutError:
                # Send periodic ping to keep connection alive
                await websocket.send_text(json.dumps({"type": "ping", "message": "Connection alive"}))
            except Exception:
                break
    except WebSocketDisconnect:
        pass
    finally:
        if connection_id in active_connections:
            del active_connections[connection_id]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Display the main form for URL input and format selection"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/download")
async def download_documentation(
    request: Request,
    url: str = Form(...),
    output_format: str = Form(...),
    connection_id: str = Form(...)
):
    """Process the documentation URL and generate the requested format"""
    
    if output_format not in ["pdf", "markdown"]:
        raise HTTPException(status_code=400, detail="Invalid output format. Choose 'pdf' or 'markdown'")
    
    # Start background task for processing
    asyncio.create_task(process_documentation_task(url, output_format, connection_id))
    
    return {"status": "started", "connection_id": connection_id}

async def process_documentation_task(url: str, output_format: str, connection_id: str):
    """Background task to process documentation"""
    
    # Initialize progress tracker
    progress = ProgressTracker(connection_id)
    
    try:
        # Step 1: Initialize
        await progress.send_progress(1, 7, "🚀 Starting documentation download", f"Initializing scraper for {url}")
        await asyncio.sleep(0.5)  # Small delay to ensure message is sent
        
        # Initialize the scraper
        scraper = DocumentationScraper(url, progress_tracker=progress)
        
        # Step 2: Begin scraping
        await progress.send_progress(2, 7, "🌐 Visiting the URL", f"Connecting to {url}")
        await asyncio.sleep(0.5)
        
        # Scrape the documentation (get all available pages)
        pages = await scraper.scrape_documentation()
        
        if not pages:
            await progress.send_progress(7, 7, "❌ No pages found", "Unable to scrape the documentation")
            return
        
        # Step 4: Processing complete
        await progress.send_progress(4, 7, "✅ Documentation extracted", f"Successfully extracted {len(pages)} pages")
        await asyncio.sleep(0.5)
        
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"documentation_{timestamp}"
        
        if output_format == "pdf":
            # Step 5: Creating PDF
            await progress.send_progress(5, 7, "📄 Creating PDF file", "Generating PDF from extracted content")
            
            filename = f"{base_filename}.pdf"
            file_path = os.path.join(OUTPUT_DIR, filename)
            await scraper.generate_pdf(pages, file_path, progress)
            
            # Copy to user's Downloads folder
            user_file_path = os.path.join(USER_DOWNLOADS_DIR, filename)
            try:
                shutil.copy2(file_path, user_file_path)
                copy_success = True
            except Exception as e:
                copy_success = False
                print(f"Warning: Could not copy to Downloads folder: {e}")
            
            # Step 6: PDF ready
            if copy_success:
                await progress.send_progress(6, 7, "✅ PDF generation complete", f"PDF saved: {filename}")
                # Step 7: Complete
                await progress.send_progress(7, 7, "📁 Check your Download folder", 
                                           f"PDF file {filename} saved to Downloads folder")
            else:
                await progress.send_progress(6, 7, "✅ PDF file created", f"File: {filename}")
                # Step 7: Complete  
                await progress.send_progress(7, 7, "🎉 Download complete!", 
                                           f"PDF file {filename} is ready for download")
        
        else:  # markdown
            # Step 5: Creating Markdown
            await progress.send_progress(5, 7, "📝 Creating Markdown file", "Converting content to Markdown format")
            
            filename = f"{base_filename}.md"
            file_path = os.path.join(OUTPUT_DIR, filename)
            await scraper.generate_markdown(pages, file_path)
            
            # Copy to user's Downloads folder
            user_file_path = os.path.join(USER_DOWNLOADS_DIR, filename)
            try:
                shutil.copy2(file_path, user_file_path)
                copy_success = True
            except Exception as e:
                copy_success = False
                print(f"Warning: Could not copy to Downloads folder: {e}")
            
            # Step 6: Markdown ready
            if copy_success:
                await progress.send_progress(6, 7, "✅ Markdown processing complete", f"Markdown saved: {filename}")
                # Step 7: Complete
                await progress.send_progress(7, 7, "📁 Check your Download folder", 
                                           f"Markdown file {filename} saved to Downloads folder")
            else:
                await progress.send_progress(6, 7, "✅ Markdown processing complete", f"File: {filename}")
                # Step 7: Complete
                await progress.send_progress(7, 7, "🎉 Download complete!", 
                                           f"Markdown file {filename} is ready for download")
    
    except Exception as e:
        await progress.send_progress(7, 7, "❌ Error occurred", f"Error processing documentation: {str(e)}")

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download the generated file"""
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/status")
async def status():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Documentation Downloader is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)