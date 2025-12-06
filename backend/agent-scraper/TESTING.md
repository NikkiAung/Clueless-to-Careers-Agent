# Testing Guide for Job Scraper

This guide will help you test the job scraper implementation.

## Prerequisites

1. **Install Dependencies**
   ```bash
   cd /Users/aungnandaoo/Desktop/clueless-to-careers-agent
   pip install -r requirements.txt
   ```

2. **Install Playwright Browsers**
   ```bash
   playwright install chromium
   ```

3. **Set Up Environment Variables**
   
   Create a `.env` file in the `backend/` directory with:
   ```
   DIGITALOCEAN_AGENT_ENDPOINT=your_endpoint_url
   DIGITALOCEAN_AGENT_ACCESS_KEY=your_access_key
   ```

## Testing Methods

### Method 1: Using the Test Script (Recommended)

The easiest way to test is using the provided test script:

```bash
cd backend/agent-scraper
python test_scraper.py
```

The script will:
1. Ask you to choose between scraping only or full integration
2. Prompt for a job posting URL
3. Display the results
4. Optionally save results to a JSON file

**Example:**
```bash
$ python test_scraper.py

Choose a test option:
1. Test scraping only (no AI agent)
2. Test full integration (scraping + AI agent)
3. Test with sample URLs
4. Exit

Enter your choice (1-4): 1
Enter job posting URL: https://www.linkedin.com/jobs/view/1234567890
```

### Method 2: Direct Python Testing

#### Test Scraping Only (No AI Agent)

```python
import asyncio
from apify_scraper import scrape_job_posting, format_job_data_for_prompt

async def test():
    url = "https://www.linkedin.com/jobs/view/YOUR_JOB_ID"
    job_data = await scrape_job_posting(url)
    print("Job Title:", job_data.get("job_title"))
    print("Company:", job_data.get("company"))
    print("Description:", job_data.get("job_description")[:200])
    
    formatted = format_job_data_for_prompt(job_data)
    print("\nFormatted Prompt:")
    print(formatted)

asyncio.run(test())
```

#### Test Full Integration (With AI Agent)

```python
from job_scraper_service import scrape_and_tailor_resume_sync

url = "https://www.linkedin.com/jobs/view/YOUR_JOB_ID"
result = scrape_and_tailor_resume_sync(url)

if result["success"]:
    print("✅ Success!")
    print("AI Response:", result["ai_response"])
else:
    print("❌ Error:", result["error"])
```

### Method 3: Command Line Testing

```bash
cd backend/agent-scraper
python job_scraper_service.py "https://www.linkedin.com/jobs/view/YOUR_JOB_ID"
```

## Test URLs

You can test with real job posting URLs from:

- **LinkedIn**: `https://www.linkedin.com/jobs/view/JOB_ID`
- **Indeed**: `https://www.indeed.com/viewjob?jk=JOB_ID`
- **Glassdoor**: `https://www.glassdoor.com/job-listing/JOB_ID`
- **Monster**: `https://www.monster.com/jobs/search?q=...`
- **ZipRecruiter**: `https://www.ziprecruiter.com/jobs/...`
- **Dice**: `https://www.dice.com/job-detail/JOB_ID`
- **Lever**: `https://jobs.lever.co/COMPANY/JOB_ID`
- **Greenhouse**: `https://boards.greenhouse.io/COMPANY/jobs/JOB_ID`

## What to Check

### ✅ Scraping Test Should Show:

1. **Job Title** - Extracted correctly
2. **Company Name** - Extracted correctly
3. **Location** - Extracted correctly
4. **Job Description** - Full or partial description
5. **Skills** - Required skills and competencies
6. **Education** - Education requirements
7. **Experience** - Experience requirements
8. **Benefits** - Compensation and benefits (if available)

### ✅ Full Integration Test Should Show:

1. All of the above scraping results
2. **Formatted Prompt** - Well-structured prompt sent to AI
3. **AI Response** - Tailored resume or recommendations from AI agent

## Troubleshooting

### Error: "Crawlee is not installed"
```bash
pip install crawlee[playwright]
```

### Error: "Playwright browser not found"
```bash
playwright install chromium
```

### Error: "Missing environment variables"
- Check that `.env` file exists in `backend/` directory
- Verify `DIGITALOCEAN_AGENT_ENDPOINT` and `DIGITALOCEAN_AGENT_ACCESS_KEY` are set

### Error: "Failed to extract sufficient job information"
- The URL might not be a valid job posting
- The job site might not be supported
- The page structure might have changed
- Try a different job posting URL

### Error: "Agent API request failed"
- Check your Digital Ocean agent endpoint URL
- Verify your access key is correct
- Check your internet connection
- Verify the agent is accessible

## Expected Output

### Successful Scraping Test:
```
================================================================================
SCRAPED DATA:
================================================================================

JOB TITLE:
Software Engineer Intern

COMPANY:
Stoke Space

LOCATION:
Kent, WA

JOB DESCRIPTION:
We know that at the heart of every great challenge is an extraordinary team...
```

### Successful Full Integration Test:
```
✅ SUCCESS!
================================================================================
JOB DATA SUMMARY:
================================================================================
Job Title: Software Engineer Intern
Company: Stoke Space
Location: Kent, WA
Description Length: 2456 characters
Skills Extracted: Yes
Education Extracted: Yes

================================================================================
AI AGENT RESPONSE:
================================================================================
[AI-generated tailored resume content...]
```

## Next Steps

After successful testing:

1. **Integrate with Backend API**: Create an API endpoint that calls `scrape_and_tailor_resume_sync()`
2. **Connect to Extension**: Update the Chrome extension to send job URLs to your backend
3. **Add Error Handling**: Implement proper error handling in your API
4. **Add Logging**: Add logging for debugging and monitoring

