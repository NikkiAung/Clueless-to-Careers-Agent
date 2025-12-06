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

   Server runs on `http://localhost:5001` (port 5001 is used to avoid conflict with macOS AirPlay Receiver on port 5000)
   
   **Note:** You can change the port by setting the `PORT` environment variable:
   ```bash
   PORT=5002 python api_server.py
   ```

3. **Use the extension:**
   - Navigate to a job posting page
   - Click extension icon → "Apply for Job"
   - Extension will send the current tab URL to the backend
   - Backend scrapes the job and returns tailored resume

## API Endpoints

### POST /api/format-resume

Format a resume PDF file using AI.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field containing PDF file

**Response:**
```json
{
  "success": true,
  "formatted_resume": {...},
  "extracted_text_length": 1234,
  "error": null
}
```

### POST /api/scrape-and-tailor

**Request:**
```json
{
  "job_url": "https://example.com/job-posting",
  "user_id": "uuid-string" // Optional: If provided, will fetch resume from Supabase parsed_resumes table
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
4. `background.js` calls `http://localhost:5001/api/scrape-and-tailor`
5. Backend calls `job_scraper_service.py` which:
   - Scrapes the job posting (Step 1: Analyzing job description)
   - Formats the data
   - Sends to AI agent
   - Returns tailored resume
6. Extension displays results

## Troubleshooting

**"Failed to connect to backend"**
- Make sure server is running: `python backend/api_server.py`
- Check it's on `http://localhost:5001` (default port)
- If you see "port already in use", try a different port: `PORT=5002 python api_server.py`
- On macOS, port 5000 is often used by AirPlay Receiver - that's why we use 5001 by default

**"Missing environment variables"**
- Create `.env` in `backend/` with:
  ```
  DIGITALOCEAN_AGENT_ENDPOINT=your_endpoint
  DIGITALOCEAN_AGENT_ACCESS_KEY=your_key
  RESUME_FORMATTER_ENDPOINT=your_resume_formatter_endpoint (optional)
  RESUME_FORMATTER_ACCESS_KEY=your_resume_formatter_key (optional)
  SUPABASE_URL=your_supabase_url (optional - for fetching resumes from database)
  SUPABASE_SERVICE_ROLE_KEY=your_service_role_key (optional - for fetching resumes from database)
  # Or use NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY if available
  ```

**"Failed to fetch" or "Cannot connect to backend API"**
- Make sure the backend server is running: `cd backend && python api_server.py`
- Check that the server is accessible at `http://localhost:5000`
- Verify CORS is enabled (should be by default)
- If using a different port, set `NEXT_PUBLIC_API_URL` in your `.env.local` file

