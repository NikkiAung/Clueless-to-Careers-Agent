"""
Test script for the job scraper service.
This script helps you test the scraper with different job posting URLs.
"""
import asyncio
import sys
import json
from pathlib import Path

# Import from the same directory
from job_scraper_service import scrape_and_tailor_resume_sync
from apify_scraper import scrape_job_posting, format_job_data_for_prompt


def test_scraping_only(url: str):
    """Test only the scraping functionality without AI agent"""
    print("=" * 80)
    print("TESTING: Scraping Only (No AI Agent)")
    print("=" * 80)
    print(f"URL: {url}\n")
    
    try:
        job_data = asyncio.run(scrape_job_posting(url))
        
        print("\n" + "=" * 80)
        print("SCRAPED DATA:")
        print("=" * 80)
        
        for key, value in job_data.items():
            if value:
                print(f"\n{key.upper().replace('_', ' ')}:")
                print("-" * 80)
                # Print first 500 characters
                if len(value) > 500:
                    print(value[:500] + "...")
                    print(f"\n[Total length: {len(value)} characters]")
                else:
                    print(value)
        
        print("\n" + "=" * 80)
        print("FORMATTED PROMPT:")
        print("=" * 80)
        formatted = format_job_data_for_prompt(job_data)
        print(formatted[:1000] + "..." if len(formatted) > 1000 else formatted)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_integration(url: str):
    """Test the full integration with AI agent"""
    print("=" * 80)
    print("TESTING: Full Integration (Scraping + AI Agent)")
    print("=" * 80)
    print(f"URL: {url}\n")
    
    try:
        result = scrape_and_tailor_resume_sync(url)
        
        if result["success"]:
            print("\n✅ SUCCESS!")
            print("=" * 80)
            print("JOB DATA SUMMARY:")
            print("=" * 80)
            job_data = result["job_data"]
            print(f"Job Title: {job_data.get('job_title', 'N/A')}")
            print(f"Company: {job_data.get('company', 'N/A')}")
            print(f"Location: {job_data.get('location', 'N/A')}")
            print(f"Description Length: {len(job_data.get('job_description', ''))} characters")
            print(f"Skills Extracted: {'Yes' if job_data.get('skills') else 'No'}")
            print(f"Education Extracted: {'Yes' if job_data.get('education') else 'No'}")
            
            print("\n" + "=" * 80)
            print("AI AGENT RESPONSE:")
            print("=" * 80)
            print(result["ai_response"])
            
            # Optionally save to file
            save = input("\n💾 Save results to file? (y/n): ").strip().lower()
            if save == 'y':
                filename = f"test_result_{job_data.get('job_title', 'job').replace(' ', '_')[:30]}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"✅ Saved to {filename}")
            
            return True
        else:
            print(f"\n❌ FAILED: {result['error']}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test function"""
    print("\n" + "=" * 80)
    print("JOB SCRAPER TEST SUITE")
    print("=" * 80)
    print("\nChoose a test option:")
    print("1. Test scraping only (no AI agent)")
    print("2. Test full integration (scraping + AI agent)")
    print("3. Test with sample URLs")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "4":
        print("Exiting...")
        return
    
    if choice == "3":
        print("\nSample job posting URLs you can test with:")
        print("- LinkedIn: https://www.linkedin.com/jobs/view/...")
        print("- Indeed: https://www.indeed.com/viewjob?jk=...")
        print("- Glassdoor: https://www.glassdoor.com/job-listing/...")
        print("\nPlease provide a real job posting URL to test.")
        choice = input("\nEnter your choice (1-2): ").strip()
    
    if choice not in ["1", "2"]:
        print("Invalid choice. Exiting...")
        return
    
    # Get URL from user
    url = input("\nEnter job posting URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting...")
        return
    
    if not url.startswith("http"):
        print("Invalid URL. Please provide a full URL starting with http:// or https://")
        return
    
    # Run the appropriate test
    if choice == "1":
        test_scraping_only(url)
    elif choice == "2":
        test_full_integration(url)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

