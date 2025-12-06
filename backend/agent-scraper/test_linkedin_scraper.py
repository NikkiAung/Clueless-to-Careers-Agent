"""
Test script to scrape LinkedIn job posting and use it with resume_planner.py
This script will:
1. Scrape the job posting from LinkedIn URL
2. Format the scraped data
3. Use it with resume_planner.py's send_prompt_to_agent function
"""
import asyncio
import sys
from pathlib import Path

# Import the scraper and resume planner
from apify_scraper import scrape_job_posting, format_job_data_for_prompt
from resume_planner import send_prompt_to_agent


async def test_linkedin_scraping_and_ai(job_url: str):
    """
    Test the full workflow: scrape LinkedIn job -> format -> send to AI agent
    
    Args:
        job_url: LinkedIn job posting URL
    """
    print("=" * 80)
    print("TESTING: LinkedIn Job Scraping + AI Agent Integration")
    print("=" * 80)
    print(f"URL: {job_url}\n")
    
    try:
        # Step 1: Scrape the job posting
        print("Step 1: Scraping job posting...")
        print("-" * 80)
        job_data = await scrape_job_posting(job_url)
        
        # Display what was scraped
        print("\n📋 SCRAPED DATA:")
        print("=" * 80)
        for key, value in job_data.items():
            if value and key != "full_text":  # Skip full_text for cleaner output
                print(f"\n{key.upper().replace('_', ' ')}:")
                if len(value) > 300:
                    print(value[:300] + "...")
                    print(f"[Total length: {len(value)} characters]")
                else:
                    print(value)
        
        # Check if we got meaningful data
        if not job_data.get("job_title") and not job_data.get("job_description"):
            print("\n⚠️  WARNING: Could not extract job information.")
            print("This might be because:")
            print("  - LinkedIn requires authentication (sign-in page detected)")
            print("  - The URL is not a direct job posting URL")
            print("  - The page structure has changed")
            print("\nTrying to use full_text as fallback...")
            
            if job_data.get("full_text"):
                # Check if it's a sign-in page
                full_text_lower = job_data["full_text"].lower()
                if "sign in" in full_text_lower or "login" in full_text_lower:
                    print("\n❌ ERROR: LinkedIn sign-in page detected. Cannot scrape without authentication.")
                    print("\n💡 SOLUTIONS:")
                    print("  1. Use a direct job posting URL (not a collections page)")
                    print("  2. Test with a public job posting from Indeed or Glassdoor")
                    print("  3. Implement LinkedIn authentication (advanced)")
                    return
                else:
                    # Use full text as job description
                    job_data["job_description"] = job_data["full_text"][:5000]  # Limit length
        
        # Step 2: Format the scraped data into a prompt
        print("\n" + "=" * 80)
        print("Step 2: Formatting scraped data into prompt...")
        print("-" * 80)
        formatted_prompt = format_job_data_for_prompt(job_data)
        
        if not formatted_prompt or len(formatted_prompt.strip()) < 50:
            print("❌ ERROR: Failed to create a valid prompt from scraped data")
            return
        
        print(f"\n✅ Formatted prompt created ({len(formatted_prompt)} characters)")
        print("\n📝 FORMATTED PROMPT (first 500 chars):")
        print("-" * 80)
        print(formatted_prompt[:500] + "..." if len(formatted_prompt) > 500 else formatted_prompt)
        
        # Step 3: Send to AI agent
        print("\n" + "=" * 80)
        print("Step 3: Sending to AI agent...")
        print("-" * 80)
        
        try:
            ai_response = send_prompt_to_agent(formatted_prompt)
            
            print("\n✅ SUCCESS! AI Agent Response:")
            print("=" * 80)
            print(ai_response)
            print("\n" + "=" * 80)
            
            # Optionally save the results
            save = input("\n💾 Save results to file? (y/n): ").strip().lower()
            if save == 'y':
                import json
                from datetime import datetime
                filename = f"test_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                result = {
                    "url": job_url,
                    "job_data": job_data,
                    "formatted_prompt": formatted_prompt,
                    "ai_response": ai_response,
                    "timestamp": datetime.now().isoformat()
                }
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"✅ Saved to {filename}")
            
        except Exception as e:
            print(f"\n❌ ERROR sending to AI agent: {e}")
            print("\nThis might be because:")
            print("  - Missing .env file with DIGITALOCEAN_AGENT_ENDPOINT and DIGITALOCEAN_AGENT_ACCESS_KEY")
            print("  - Invalid credentials")
            print("  - Network connection issue")
            print("\nBut the scraping worked! Here's the formatted prompt you can use:")
            print("\n" + "=" * 80)
            print("FORMATTED PROMPT (ready to use):")
            print("=" * 80)
            print(formatted_prompt)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function"""
    # Default URL from user's request
    default_url = "https://www.linkedin.com/jobs/collections/top-applicant/?currentJobId=4325312273&originToLandingJobPostings=4324998975%2C4325312273"
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print(f"Using default URL: {default_url}")
        print("(You can also pass a URL as argument: python test_linkedin_scraper.py <URL>)")
        url = default_url
    
    # Run the async test
    asyncio.run(test_linkedin_scraping_and_ai(url))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

