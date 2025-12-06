"""
Service that integrates job scraping with resume planning.
This module provides a high-level interface for scraping job postings
and sending them to the AI agent for resume tailoring.
"""
import asyncio
import sys
import os
import json
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import from the same directory
from resume_planner import send_prompt_to_agent
from apify_scraper import scrape_job_posting, format_job_data_for_prompt
from getting_user_resume_data import get_user_resume_text, fetch_resume_from_supabase, convert_parsed_resume_to_text

# Import from parent directory (backend/user_job_match and backend/tailor_resume)
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from user_job_match.user_job_map import ask_agent_for_improvements
from tailor_resume.rewrite_resume import rewrite_resume_with_agent

# Optional import for PDF conversion - server can start without it
try:
    from convertMDtoPDF.convertoPDF import convert_markdown_to_pdf
    PDF_CONVERSION_AVAILABLE = True
except (ImportError, OSError) as e:
    print(f"Warning: PDF conversion not available: {e}")
    print("PDF generation will be skipped. To enable it, install WeasyPrint dependencies:")
    print("  macOS: brew install pango gdk-pixbuf gobject-introspection")
    print("  Then: pip install --upgrade weasyprint")
    PDF_CONVERSION_AVAILABLE = False
    convert_markdown_to_pdf = None


# Resume retrieval functions are now imported from getting_user_resume_data.py
# This keeps the code modular and separates concerns


async def scrape_and_tailor_resume(job_url: str, resume_text: str = None, user_id: str = None) -> dict:
    """
    Main function that scrapes a job posting and sends it to the AI agent.
    
    This function:
    1. Scrapes the job posting from the given URL
    2. Formats the scraped data into a prompt
    3. Sends the prompt to the AI agent for resume planning (job insights)
    4. Gets improvement suggestions by matching resume to job posting
    5. Rewrites the resume based on improvements
    6. Returns all the data and responses
    
    Args:
        job_url (str): URL of the job posting to scrape
        resume_text (str, optional): The resume text to use. If not provided, tries to fetch from Supabase using user_id, or falls back to example_resume.
        user_id (str, optional): User UUID to fetch resume from Supabase database.
        
    Returns:
        dict: Dictionary containing:
            - success (bool): Whether the operation was successful
            - job_data (dict): Scraped job information
            - formatted_prompt (str): The formatted prompt sent to AI
            - ai_response (str): The AI agent's response (job insights)
            - improvements (str): Improvement suggestions from user-job match agent
            - rewritten_resume (str): The rewritten resume (Markdown)
            - pdf_path (str): Path to the generated PDF file
            - error (str): Error message if any
    """
    # Initialize result dictionary first (before any early returns)
    result = {
        "success": False,
        "job_data": {},
        "formatted_prompt": "",
        "ai_response": "",
        "improvements": "",
        "rewritten_resume": "",
        "pdf_path": "",
        "error": ""
    }
    
    # Determine which resume to use
    resume = None
    
    if resume_text:
        # Use provided resume text
        resume = resume_text
    elif user_id:
        # Try to fetch from Supabase using the imported function
        print(f"\n{'='*80}")
        print(f"Fetching resume from Supabase for user_id: {user_id}")
        print(f"{'='*80}")
        resume = get_user_resume_text(user_id)
        if resume:
            print("✓ Resume found in database, converted to text format")
            print(f"Resume text length: {len(resume)} characters")
        else:
            print("⚠ No resume found in database for this user_id")
            print("⚠ Cannot proceed without resume data. Please upload a resume first.")
            result["error"] = "No resume found in database. Please upload a resume first."
            return result
    else:
        # No user_id provided and no resume_text
        print("⚠ No user_id provided and no resume_text")
        print("⚠ Cannot proceed without resume data. Please provide user_id or resume_text.")
        result["error"] = "No resume data provided. Please provide user_id or resume_text."
        return result
    
    try:
        # Step 1: Scrape the job posting
        print(f"\n{'='*80}")
        print(f"STEP 1: Scraping job posting from: {job_url}")
        print(f"{'='*80}")
        job_data = await scrape_job_posting(job_url)
        result["job_data"] = job_data
        
        print(f"\nScraping completed. Extracted data:")
        print(f"  - Job Title: {job_data.get('job_title', 'N/A')}")
        print(f"  - Company: {job_data.get('company', 'N/A')}")
        print(f"  - Location: {job_data.get('location', 'N/A')}")
        print(f"  - Description: {len(job_data.get('job_description', ''))} chars")
        print(f"  - Full Text: {len(job_data.get('full_text', ''))} chars")
        
        # Step 2: Format the scraped data into a prompt
        print(f"\n{'='*80}")
        print(f"STEP 2: Formatting scraped data into prompt")
        print(f"{'='*80}")
        formatted_prompt = format_job_data_for_prompt(job_data)
        result["formatted_prompt"] = formatted_prompt
        print(f"Formatted prompt length: {len(formatted_prompt)} characters")
        print(f"Prompt preview (first 200 chars): {formatted_prompt[:200]}...")
        
        # Check if we got any meaningful data
        has_data = (
            job_data.get("job_title") or 
            job_data.get("job_description") or 
            (job_data.get("full_text") and len(job_data.get("full_text", "")) > 200)
        )
        
        if not has_data:
            # Provide more detailed error message
            full_text_len = len(job_data.get("full_text", ""))
            error_details = []
            if full_text_len == 0:
                error_details.append("No content was extracted from the page")
            elif full_text_len < 100:
                error_details.append(f"Only {full_text_len} characters were extracted (likely a login page or blocked content)")
            else:
                error_details.append(f"Extracted {full_text_len} characters but couldn't identify job-specific information")
            
            if not job_data.get("job_title"):
                error_details.append("Could not find job title")
            if not job_data.get("job_description"):
                error_details.append("Could not find job description")
            
            error_msg = "Failed to extract sufficient job information from the URL. " + "; ".join(error_details) + ". The page might require authentication, have anti-scraping measures, or use a different structure than expected."
            result["error"] = error_msg
            print(f"\n❌ {error_msg}")
            print(f"Full text preview (first 500 chars): {job_data.get('full_text', '')[:500]}")
            return result
        
        # If we have full_text but no formatted prompt, use full_text
        if not formatted_prompt or len(formatted_prompt.strip()) < 50:
            if job_data.get("full_text") and len(job_data.get("full_text", "")) > 200:
                # Use full_text as the prompt if we have it
                formatted_prompt = f"Job Posting:\n\n{job_data['full_text']}"
                result["formatted_prompt"] = formatted_prompt
            else:
                result["error"] = "Failed to extract sufficient job information from the URL"
                return result
        
        # Step 3: Send to AI agent
        print(f"\n{'='*80}")
        print(f"STEP 3: Sending to AI agent")
        print(f"{'='*80}")
        print("Sending job information to AI agent...")
        ai_response = send_prompt_to_agent(formatted_prompt)
        result["ai_response"] = ai_response
        result["success"] = True
        
        print(f"\n✓ AI Agent Response Received!")
        print(f"Response length: {len(ai_response)} characters")
        print(f"\nAI Response Preview (first 500 chars):")
        print(ai_response)
        
        # Check if response is JSON
        if ai_response.strip().startswith('{') or ai_response.strip().startswith('['):
            print(f"\n✓ Response appears to be JSON format")
        else:
            print(f"\n⚠ Response is not JSON format")
        
        # Step 4: Get improvement suggestions by matching resume to job posting
        print(f"\n{'='*80}")
        print(f"STEP 4: Getting improvement suggestions")
        print(f"{'='*80}")
        try:
            improvements_prompt = f"Resume: {resume} + Job Insights: {ai_response}"
            improvements = ask_agent_for_improvements(improvements_prompt)
            result["improvements"] = improvements
            print(f"\n✓ Improvements Received!")
            print(f"Improvements length: {len(improvements)} characters")
            print(f"\nImprovements Preview (first 500 chars):")
            print(improvements)
        except Exception as e:
            error_msg = f"Failed to get improvements: {str(e)}"
            result["error"] = error_msg
            print(f"\n❌ {error_msg}")
        
        # Step 5: Rewrite resume based on improvements
        print(f"\n{'='*80}")
        print(f"STEP 5: Rewriting resume")
        print(f"{'='*80}")
        try:
            rewritten_resume_prompt = f"Improvements: {result.get('improvements', '')} + Resume: {resume}"
            rewritten_resume = rewrite_resume_with_agent(rewritten_resume_prompt)
            result["rewritten_resume"] = rewritten_resume
            print(f"\n✓ Resume Rewritten!")
            print(f"Rewritten resume length: {len(rewritten_resume)} characters")
            print(f"\nRewritten Resume Preview (first 500 chars):")
            print(rewritten_resume)
        except Exception as e:
            error_msg = f"Failed to rewrite resume: {str(e)}"
            if result["error"]:
                result["error"] += f" | {error_msg}"
            else:
                result["error"] = error_msg
            print(f"\n❌ {error_msg}")
        
        # Step 6: Convert rewritten resume (Markdown) to PDF
        print(f"\n{'='*80}")
        print(f"STEP 6: Converting Markdown to PDF")
        print(f"{'='*80}")
        if result.get("rewritten_resume"):
            if not PDF_CONVERSION_AVAILABLE or not convert_markdown_to_pdf:
                print(f"\n⚠ PDF conversion not available. Skipping PDF generation.")
                print("To enable PDF generation, install WeasyPrint dependencies:")
                print("  macOS: brew install pango gdk-pixbuf gobject-introspection")
                print("  Then: pip install --upgrade weasyprint")
            else:
                try:
                    # Generate output PDF path
                    # Use job title or company name for filename if available
                    job_title = result.get("job_data", {}).get("job_title", "resume")
                    company = result.get("job_data", {}).get("company", "")
                    
                    # Sanitize filename
                    safe_job_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
                    safe_company = "".join(c for c in company if c.isalnum() or c in (' ', '-', '_')).strip()[:30]
                    
                    if safe_company:
                        pdf_filename = f"tailored_resume_{safe_job_title}_{safe_company}.pdf"
                    else:
                        pdf_filename = f"tailored_resume_{safe_job_title}.pdf"
                    
                    # Remove spaces and replace with underscores
                    pdf_filename = pdf_filename.replace(" ", "_")
                    
                    # Set output path in the convertMDtoPDF directory
                    output_dir = backend_path / "convertMDtoPDF"
                    output_dir.mkdir(parents=True, exist_ok=True)
                    pdf_path = output_dir / pdf_filename
                    
                    print(f"Converting Markdown to PDF: {pdf_path}")
                    pdf_path_str = convert_markdown_to_pdf(
                        markdown_content=result["rewritten_resume"],
                        output_path=pdf_path
                    )
                    # Convert to relative path from backend directory for API endpoint
                    pdf_path_relative = Path(pdf_path_str).relative_to(backend_path)
                    result["pdf_path"] = str(pdf_path_relative)
                    print(f"\n✓ PDF Generated Successfully!")
                    print(f"PDF saved at: {pdf_path_str}")
                    print(f"Relative path (for API): {result['pdf_path']}")
                except Exception as e:
                    error_msg = f"Failed to convert to PDF: {str(e)}"
                    if result["error"]:
                        result["error"] += f" | {error_msg}"
                    else:
                        result["error"] = error_msg
                    print(f"\n❌ {error_msg}")
                    import traceback
                    traceback.print_exc()
        else:
            print(f"\n⚠ Skipping PDF conversion: No rewritten resume available")
        
        print(f"\n{'='*80}")
        print("Process completed!")
        print(f"{'='*80}\n")
        return result
        
    except Exception as e:
        result["error"] = str(e)
        print(f"Error: {e}")
        return result


def scrape_and_tailor_resume_sync(job_url: str, resume_text: str = None, user_id: str = None) -> dict:
    """
    Synchronous wrapper for scrape_and_tailor_resume.
    
    This is useful when calling from non-async contexts (like Flask/FastAPI endpoints).
    
    Uses a thread pool executor to run the async code in a separate thread with its own
    event loop, preventing conflicts with Playwright/Crawlee locks that may be bound
    to different event loops.
    
    Args:
        job_url (str): URL of the job posting to scrape
        resume_text (str, optional): The resume text to use. If not provided, tries to fetch from Supabase using user_id, or falls back to example_resume.
        user_id (str, optional): User UUID to fetch resume from Supabase database.
        
    Returns:
        dict: Same as scrape_and_tailor_resume
    """
    def run_in_thread():
        """Run the async function in a new thread with its own event loop."""
        # Create a completely new event loop in this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(scrape_and_tailor_resume(job_url, resume_text, user_id))
        finally:
            # Clean up: close the loop and remove it
            loop.close()
            asyncio.set_event_loop(None)
    
    # Use ThreadPoolExecutor to run in a separate thread
    # This ensures we have a completely isolated event loop
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_in_thread)
        return future.result()


if __name__ == "__main__":
    """Test the service"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python job_scraper_service.py <job_url>")
        sys.exit(1)
    
    job_url = sys.argv[1]
    result = scrape_and_tailor_resume_sync(job_url)
    

