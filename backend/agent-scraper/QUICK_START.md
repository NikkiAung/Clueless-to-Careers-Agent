# Quick Start Testing Guide

## Step 1: Install Dependencies

```bash
cd /Users/aungnandaoo/Desktop/clueless-to-careers-agent
pip install -r requirements.txt
playwright install chromium
```

## Step 2: Set Up Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cd backend
cat > .env << EOF
DIGITALOCEAN_AGENT_ENDPOINT=your_endpoint_url_here
DIGITALOCEAN_AGENT_ACCESS_KEY=your_access_key_here
EOF
```

Replace `your_endpoint_url_here` and `your_access_key_here` with your actual values.

## Step 3: Test the Scraper

### Option A: Interactive Test Script (Easiest)

```bash
cd backend/agent-scraper
python test_scraper.py
```

Follow the prompts:
1. Choose option 1 to test scraping only (no AI agent needed)
2. Or choose option 2 to test full integration (requires AI agent setup)
3. Enter a job posting URL when prompted

### Option B: Quick Command Line Test

```bash
cd backend/agent-scraper

# Test scraping only (no AI agent)
python -c "
import asyncio
from apify_scraper import scrape_job_posting
url = 'YOUR_JOB_URL_HERE'
result = asyncio.run(scrape_job_posting(url))
print('Job Title:', result.get('job_title'))
print('Company:', result.get('company'))
"

# Test full integration (requires AI agent)
python job_scraper_service.py "YOUR_JOB_URL_HERE"
```

## Step 4: Verify Results

You should see:
- ✅ Job title extracted
- ✅ Company name extracted
- ✅ Job description extracted
- ✅ Skills/requirements extracted (if available)
- ✅ AI response (if testing full integration)

## Common Issues

**Issue**: `ModuleNotFoundError: No module named 'crawlee'`
**Solution**: `pip install crawlee[playwright]`

**Issue**: `Browser not found`
**Solution**: `playwright install chromium`

**Issue**: `Missing environment variables`
**Solution**: Create `.env` file in `backend/` directory

**Issue**: `Failed to extract job information`
**Solution**: Try a different job posting URL or check if the URL is accessible

## Example Test URLs

You can test with any public job posting URL. Here are some examples:

- LinkedIn: `https://www.linkedin.com/jobs/view/...`
- Indeed: `https://www.indeed.com/viewjob?jk=...`
- Glassdoor: `https://www.glassdoor.com/job-listing/...`

**Note**: Make sure the URL is publicly accessible (not behind login).

