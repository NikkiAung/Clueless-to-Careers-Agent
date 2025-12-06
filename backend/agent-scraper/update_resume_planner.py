"""
Script to update resume_planner.py with scraped job data.
This will scrape a job posting and update the user_prompt variable in resume_planner.py
"""
import asyncio
import sys
import re
from pathlib import Path

from apify_scraper import scrape_job_posting, format_job_data_for_prompt


async def update_resume_planner_with_scraped_data(job_url: str):
    """
    Scrape job posting and update resume_planner.py's user_prompt variable
    
    Args:
        job_url: URL of the job posting to scrape
    """
    print("=" * 80)
    print("UPDATING resume_planner.py WITH SCRAPED JOB DATA")
    print("=" * 80)
    print(f"URL: {job_url}\n")
    
    try:
        # Step 1: Scrape the job posting
        print("Step 1: Scraping job posting...")
        job_data = await scrape_job_posting(job_url)
        
        # Step 2: Format the data
        print("Step 2: Formatting data...")
        formatted_prompt = format_job_data_for_prompt(job_data)
        
        if not formatted_prompt or len(formatted_prompt.strip()) < 50:
            print("❌ ERROR: Failed to extract sufficient job information")
            return
        
        # Step 3: Read resume_planner.py
        print("Step 3: Reading resume_planner.py...")
        resume_planner_path = Path(__file__).parent / "resume_planner.py"
        
        with open(resume_planner_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Step 4: Find and replace the user_prompt variable
        print("Step 4: Updating user_prompt variable...")
        
        # Pattern to match: user_prompt = """..."""
        # This regex matches the triple-quoted string
        pattern = r'(user_prompt\s*=\s*)"""(.*?)"""'
        
        # Escape the formatted_prompt for use in triple quotes
        escaped_prompt = formatted_prompt.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')
        
        # Replace the content
        new_content = re.sub(
            pattern,
            f'\\1"""\n{escaped_prompt}\n    """',
            content,
            flags=re.DOTALL
        )
        
        # Check if replacement was made
        if new_content == content:
            print("⚠️  WARNING: Could not find user_prompt variable to replace")
            print("The file might have a different structure.")
            return
        
        # Step 5: Write the updated content
        print("Step 5: Writing updated resume_planner.py...")
        
        # Create backup
        backup_path = resume_planner_path.with_suffix('.py.backup')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Backup created: {backup_path}")
        
        # Write new content
        with open(resume_planner_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ SUCCESS! resume_planner.py has been updated")
        print(f"\n📝 Updated user_prompt with {len(formatted_prompt)} characters of scraped data")
        print("\nYou can now run resume_planner.py to test with the scraped data:")
        print("  python resume_planner.py")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function"""
    default_url = "https://www.linkedin.com/jobs/collections/top-applicant/?currentJobId=4325312273&originToLandingJobPostings=4324998975%2C4325312273"
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print(f"Using default URL: {default_url}")
        print("(You can also pass a URL as argument: python update_resume_planner.py <URL>)")
        url = default_url
    
    asyncio.run(update_resume_planner_with_scraped_data(url))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

