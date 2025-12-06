"""
Backend API server for job scraping and resume tailoring.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path

# Add agent-scraper to path
agent_scraper_path = Path(__file__).parent / "agent-scraper"
sys.path.insert(0, str(agent_scraper_path))

from job_scraper_service import scrape_and_tailor_resume_sync

app = Flask(__name__)
# Enable CORS for Chrome extension with specific settings
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})


@app.route('/api/scrape-and-tailor', methods=['POST', 'OPTIONS'])
def scrape_and_tailor():
    """
    Scrape job posting and tailor resume.
    
    Expected JSON: {"job_url": "https://example.com/job"}
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
    
    try:
        data = request.get_json()
        
        if not data or 'job_url' not in data:
            return jsonify({
                "success": False,
                "job_data": {},
                "formatted_prompt": "",
                "ai_response": "",
                "error": "Missing 'job_url' in request body"
            }), 400
        
        job_url = data['job_url']
        print(f"\n{'='*80}")
        print(f"Received request to scrape: {job_url}")
        print(f"{'='*80}\n")
        
        # Scrape and tailor resume
        result = scrape_and_tailor_resume_sync(job_url)
        
        # Log the scraping results
        print(f"\n{'='*80}")
        print("SCRAPING RESULTS:")
        print(f"{'='*80}")
        print(f"Success: {result.get('success')}")
        print(f"\nJob Data Extracted:")
        job_data = result.get('job_data', {})
        print(f"  - Job Title: {job_data.get('job_title', 'N/A')}")
        print(f"  - Company: {job_data.get('company', 'N/A')}")
        print(f"  - Location: {job_data.get('location', 'N/A')}")
        print(f"  - Description Length: {len(job_data.get('job_description', ''))} chars")
        print(f"  - Full Text Length: {len(job_data.get('full_text', ''))} chars")
        print(f"  - Skills Extracted: {'Yes' if job_data.get('skills') else 'No'}")
        print(f"  - Education Extracted: {'Yes' if job_data.get('education') else 'No'}")
        
        print(f"\nFormatted Prompt Length: {len(result.get('formatted_prompt', ''))} chars")
        if result.get('formatted_prompt'):
            print(f"Formatted Prompt Preview (first 300 chars):")
            print(result.get('formatted_prompt', '')[:300] + "...")
        
        print(f"\n{'='*80}")
        print("AI AGENT RESPONSE:")
        print(f"{'='*80}")
        ai_response = result.get('ai_response', '')
        if ai_response:
            print(f"Response Length: {len(ai_response)} characters")
            print(f"\nAI Response Preview (first 500 chars):")
            print(ai_response[:500] + "..." if len(ai_response) > 500 else ai_response)
            
            # Check if response is JSON-like
            if ai_response.strip().startswith('{') or ai_response.strip().startswith('['):
                print(f"\n✓ AI Response appears to be JSON format")
            else:
                print(f"\n⚠ AI Response is not JSON format (starts with: {ai_response[:50]}...)")
        else:
            print("No AI response received")
        
        if result.get('error'):
            print(f"\n❌ Error: {result.get('error')}")
        
        print(f"{'='*80}\n")
        
        # Ensure all required fields are present
        if "job_data" not in result:
            result["job_data"] = {}
        if "formatted_prompt" not in result:
            result["formatted_prompt"] = ""
        if "ai_response" not in result:
            result["ai_response"] = ""
        if "error" not in result:
            result["error"] = ""
        
        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in scrape_and_tailor: {error_trace}")
        return jsonify({
            "success": False,
            "job_data": {},
            "formatted_prompt": "",
            "ai_response": "",
            "error": f"Error: {str(e)}"
        }), 500


if __name__ == '__main__':
    print("Starting API server on http://localhost:5000")
    app.run(host='localhost', port=5000, debug=True)

