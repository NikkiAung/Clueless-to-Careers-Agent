"""
Service that integrates job scraping with resume planning.
This module provides a high-level interface for scraping job postings
and sending them to the AI agent for resume tailoring.
"""
import asyncio
import sys
import os
from pathlib import Path

# Import from the same directory
from resume_planner import send_prompt_to_agent
from apify_scraper import scrape_job_posting, format_job_data_for_prompt


async def scrape_and_tailor_resume(job_url: str) -> dict:
    """
    Main function that scrapes a job posting and sends it to the AI agent.
    
    This function:
    1. Scrapes the job posting from the given URL
    2. Formats the scraped data into a prompt
    3. Sends the prompt to the AI agent for resume tailoring
    4. Returns both the scraped data and the AI response
    
    Args:
        job_url (str): URL of the job posting to scrape
        
    Returns:
        dict: Dictionary containing:
            - success (bool): Whether the operation was successful
            - job_data (dict): Scraped job information
            - formatted_prompt (str): The formatted prompt sent to AI
            - ai_response (str): The AI agent's response
            - error (str): Error message if any
    """
    result = {
        "success": False,
        "job_data": {},
        "formatted_prompt": "",
        "ai_response": "",
        "error": ""
    }
    
    try:
        # Step 1: Scrape the job posting
        print(f"Scraping job posting from: {job_url}")
        job_data = await scrape_job_posting(job_url)
        result["job_data"] = job_data
        
        # Step 2: Format the scraped data into a prompt
        formatted_prompt = format_job_data_for_prompt(job_data)
        result["formatted_prompt"] = formatted_prompt
        
        if not formatted_prompt or len(formatted_prompt.strip()) < 50:
            result["error"] = "Failed to extract sufficient job information from the URL"
            return result
        
        # Step 3: Send to AI agent
        print("Sending job information to AI agent...")
        ai_response = send_prompt_to_agent(formatted_prompt)
        result["ai_response"] = ai_response
        result["success"] = True
        
        print("Successfully tailored resume!")
        return result
        
    except Exception as e:
        result["error"] = str(e)
        print(f"Error: {e}")
        return result


def scrape_and_tailor_resume_sync(job_url: str) -> dict:
    """
    Synchronous wrapper for scrape_and_tailor_resume.
    
    This is useful when calling from non-async contexts (like Flask/FastAPI endpoints).
    
    Args:
        job_url (str): URL of the job posting to scrape
        
    Returns:
        dict: Same as scrape_and_tailor_resume
    """
    return asyncio.run(scrape_and_tailor_resume(job_url))


if __name__ == "__main__":
    """Test the service"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python job_scraper_service.py <job_url>")
        sys.exit(1)
    
    job_url = sys.argv[1]
    result = scrape_and_tailor_resume_sync(job_url)
    
    if result["success"]:
        print("\n" + "=" * 80)
        print("AI RESPONSE:")
        print("=" * 80)
        print(result["ai_response"])
    else:
        print(f"\nError: {result['error']}")

