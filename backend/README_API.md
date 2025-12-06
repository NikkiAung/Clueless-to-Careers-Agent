# Backend API Server

Simple Flask API server that connects the Chrome extension to the job scraper.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install flask flask-cors
   ```

2. **Start the server:**
   ```bash
   cd backend
   python api_server.py
   ```

   Server runs on `http://localhost:5000`

3. **Use the extension:**
   - Navigate to a job posting page
   - Click extension icon → "Apply for Job"
   - Extension will send the current tab URL to the backend
   - Backend scrapes the job and returns tailored resume

## API Endpoint

### POST /api/scrape-and-tailor

**Request:**
```json
{
  "job_url": "https://example.com/job-posting"
}
```

**Response:**
```json
{
  "success": true,
  "job_data": {...},
  "formatted_prompt": "...",
  "ai_response": "...",
  "error": ""
}
```

## How It Works

1. User clicks "Apply for Job" in extension
2. Extension gets current tab URL
3. Sends URL to `background.js`
4. `background.js` calls `http://localhost:5000/api/scrape-and-tailor`
5. Backend calls `job_scraper_service.py` which:
   - Scrapes the job posting (Step 1: Analyzing job description)
   - Formats the data
   - Sends to AI agent
   - Returns tailored resume
6. Extension displays results

## Troubleshooting

**"Failed to connect to backend"**
- Make sure server is running: `python backend/api_server.py`
- Check it's on `http://localhost:5000`

**"Missing environment variables"**
- Create `.env` in `backend/` with:
  ```
  DIGITALOCEAN_AGENT_ENDPOINT=your_endpoint
  DIGITALOCEAN_AGENT_ACCESS_KEY=your_key
  ```

