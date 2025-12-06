# Job Scraper Service

This module provides functionality to scrape job postings from various job sites and send them to the AI agent for resume tailoring.

## Features

- **Multi-site support**: Supports scraping from LinkedIn, Indeed, Glassdoor, Monster, ZipRecruiter, CareerBuilder, Dice, AngelList, Stack Overflow, RemoteOK, We Work Remotely, Lever, Greenhouse, Workday, and generic job sites
- **Structured extraction**: Extracts job title, company, location, description, responsibilities, skills, education, experience, and benefits
- **AI integration**: Automatically formats scraped data and sends it to the Digital Ocean Gradient AI agent for resume tailoring

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

3. Set up environment variables in `.env` file:
```
DIGITALOCEAN_AGENT_ENDPOINT=your_endpoint_url
DIGITALOCEAN_AGENT_ACCESS_KEY=your_access_key
```

## Usage

### Basic Usage

```python
from job_scraper_service import scrape_and_tailor_resume_sync

# Scrape and tailor resume for a job posting
result = scrape_and_tailor_resume_sync("https://www.linkedin.com/jobs/view/123456")

if result["success"]:
    print("Job Data:", result["job_data"])
    print("AI Response:", result["ai_response"])
else:
    print("Error:", result["error"])
```

### Async Usage

```python
import asyncio
from job_scraper_service import scrape_and_tailor_resume

async def main():
    result = await scrape_and_tailor_resume("https://www.linkedin.com/jobs/view/123456")
    print(result)

asyncio.run(main())
```

### Command Line Usage

```bash
python job_scraper_service.py "https://www.linkedin.com/jobs/view/123456"
```

### Direct Scraping (without AI)

```python
from apify_scraper import scrape_job_posting, format_job_data_for_prompt
import asyncio

async def main():
    job_data = await scrape_job_posting("https://www.linkedin.com/jobs/view/123456")
    formatted = format_job_data_for_prompt(job_data)
    print(formatted)

asyncio.run(main())
```

## Supported Job Sites

- LinkedIn Jobs
- Indeed
- Glassdoor
- Monster
- ZipRecruiter
- CareerBuilder
- Dice
- AngelList / Wellfound
- Stack Overflow Jobs
- RemoteOK
- We Work Remotely
- Lever
- Greenhouse
- Workday
- Generic job sites (fallback)

## Return Format

The `scrape_and_tailor_resume` function returns a dictionary with:

```python
{
    "success": bool,              # Whether the operation succeeded
    "job_data": {                 # Scraped job information
        "job_title": str,
        "company": str,
        "location": str,
        "job_description": str,
        "responsibilities": str,
        "skills": str,
        "education": str,
        "experience": str,
        "benefits": str,
        "full_text": str
    },
    "formatted_prompt": str,      # Formatted prompt sent to AI
    "ai_response": str,           # AI agent's response
    "error": str                  # Error message if any
}
```

## Integration with Extension

When a user clicks "Apply for Job" in the Chrome extension:

1. The extension sends the current tab URL to the backend
2. The backend calls `scrape_and_tailor_resume_sync(job_url)`
3. The scraper extracts job information
4. The data is formatted and sent to the AI agent
5. The AI response (tailored resume) is returned to the extension

## Error Handling

The service includes comprehensive error handling:
- Invalid URLs
- Network timeouts
- Missing page elements
- AI agent connection failures
- Missing environment variables

All errors are returned in the `error` field of the result dictionary.

