"""
Backend API server for job scraping and resume tailoring.
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
import json
import tempfile
from pathlib import Path

# Add agent-scraper to path
agent_scraper_path = Path(__file__).parent / "agent-scraper"
sys.path.insert(0, str(agent_scraper_path))

# Add resume_formatter to path
resume_formatter_path = Path(__file__).parent / "resume_formatter"
sys.path.insert(0, str(resume_formatter_path))

from job_scraper_service import scrape_and_tailor_resume_sync
from pdfToText import extract_text_from_pdf
from resume_formatter import format_resume_with_agent

app = Flask(__name__)
# Enable CORS for Chrome extension and web app with specific settings
# Allow all origins for development
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})
# Also add CORS headers globally as a fallback
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    return response

# Configure upload settings
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify server is running."""
    return jsonify({
        "status": "ok",
        "message": "Backend API server is running",
        "endpoints": ["/api/format-resume", "/api/scrape-and-tailor"]
    }), 200


@app.route('/api/scrape-and-tailor', methods=['POST', 'OPTIONS'])
def scrape_and_tailor():
    """
    Scrape job posting and tailor resume.
    
    Expected JSON: {
        "job_url": "https://example.com/job",
        "user_id": "uuid-string" (optional - if provided, will fetch resume from Supabase)
    }
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
        user_id = data.get('user_id')  # Optional: user_id to fetch resume from Supabase
        
        print(f"\n{'='*80}")
        print(f"Received request to scrape: {job_url}")
        if user_id:
            print(f"User ID provided: {user_id} (will fetch resume from Supabase)")
        else:
            print("No user_id provided (will use example resume)")
        print(f"{'='*80}\n")
        
        # Scrape and tailor resume
        result = scrape_and_tailor_resume_sync(job_url, user_id=user_id)
        
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
        if "improvements" not in result:
            result["improvements"] = ""
        if "rewritten_resume" not in result:
            result["rewritten_resume"] = ""
        if "pdf_path" not in result:
            result["pdf_path"] = ""
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


@app.route('/api/format-resume', methods=['POST', 'OPTIONS'])
def format_resume():
    """
    Upload and format a resume PDF file.
    
    Expected: multipart/form-data with 'file' field containing PDF file
    Returns: JSON with formatted resume data
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "formatted_resume": None,
            "error": "No file provided. Please upload a PDF file."
        }), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({
            "success": False,
            "formatted_resume": None,
            "error": "No file selected."
        }), 400
    
    # Check file extension
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "formatted_resume": None,
            "error": "Invalid file type. Only PDF files are allowed."
        }), 400
    
    # Create temporary file to save uploaded PDF
    temp_file = None
    try:
        print(f"\n{'='*80}")
        print(f"Received resume upload request: {file.filename}")
        print(f"{'='*80}\n")
        
        # Save uploaded file to temporary location
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=f'.{file_ext}',
            dir=UPLOAD_FOLDER
        )
        file.save(temp_file.name)
        temp_file.close()
        
        print(f"Saved uploaded file to: {temp_file.name}")
        
        # Extract text from PDF
        print("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(temp_file.name)
        print(f"Extracted {len(extracted_text)} characters from PDF")
        
        # Format the resume using AI agent
        print("Formatting resume with AI agent...")
        user_prompt = f"""Format this resume:

{extracted_text}

Please format this resume in a professional, clean, and well-structured format."""
        
        formatted_resume = format_resume_with_agent(user_prompt)
        
        print(f"\n{'='*80}")
        print("RESUME FORMATTING RESULTS:")
        print(f"{'='*80}")
        print(f"Formatted resume length: {len(formatted_resume)} characters")
        if formatted_resume.strip().startswith('{') or formatted_resume.strip().startswith('['):
            print("✓ Formatted resume appears to be JSON format")
        else:
            print("⚠ Formatted resume is not JSON format")
        print(f"{'='*80}\n")
        
        # Try to parse as JSON if it's JSON format
        formatted_json = None
        try:
            formatted_json = json.loads(formatted_resume)
            print(f"\n{'='*80}")
            print("PARSED JSON OUTPUT:")
            print(f"{'='*80}")
            print(json.dumps(formatted_json, indent=2, ensure_ascii=False))
            print(f"{'='*80}\n")
        except json.JSONDecodeError as e:
            # If it's not valid JSON, return as string
            print(f"\n⚠ Warning: Could not parse as JSON: {e}")
            print(f"Raw output (first 500 chars):\n{formatted_resume[:500]}")
            formatted_json = formatted_resume
        
        return jsonify({
            "success": True,
            "formatted_resume": formatted_json,
            "extracted_text_length": len(extracted_text),
            "error": None
        }), 200
        
    except FileNotFoundError as e:
        error_msg = f"PDF file not found: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({
            "success": False,
            "formatted_resume": None,
            "error": error_msg
        }), 400
        
    except ValueError as e:
        error_msg = f"Invalid file: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({
            "success": False,
            "formatted_resume": None,
            "error": error_msg
        }), 400
        
    except RuntimeError as e:
        error_msg = f"Failed to extract text from PDF: {str(e)}"
        print(f"Error: {error_msg}")
        return jsonify({
            "success": False,
            "formatted_resume": None,
            "error": error_msg
        }), 500
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_msg = f"Error processing resume: {str(e)}"
        print(f"Error in format_resume: {error_trace}")
        return jsonify({
            "success": False,
            "formatted_resume": None,
            "error": error_msg
        }), 500
        
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file.name):
            try:
                os.unlink(temp_file.name)
                print(f"Cleaned up temporary file: {temp_file.name}")
            except Exception as e:
                print(f"Warning: Could not delete temporary file {temp_file.name}: {e}")


@app.route('/api/download-resume', methods=['GET', 'OPTIONS'])
def download_resume():
    """
    Download a tailored resume PDF file.
    
    Query parameters:
        - pdf_path: Relative path to the PDF file (from backend directory)
    
    Returns:
        PDF file for download
    """
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, OPTIONS')
        return response
    
    try:
        pdf_path = request.args.get('pdf_path')
        
        if not pdf_path:
            return jsonify({
                "success": False,
                "error": "Missing 'pdf_path' query parameter"
            }), 400
        
        # Construct full path to PDF file
        # pdf_path is relative to backend directory
        backend_dir = Path(__file__).parent
        full_pdf_path = backend_dir / pdf_path
        
        # Security check: ensure the path is within backend directory
        try:
            full_pdf_path = full_pdf_path.resolve()
            backend_dir_resolved = backend_dir.resolve()
            if not str(full_pdf_path).startswith(str(backend_dir_resolved)):
                return jsonify({
                    "success": False,
                    "error": "Invalid path: Path must be within backend directory"
                }), 403
        except (OSError, ValueError) as e:
            return jsonify({
                "success": False,
                "error": f"Invalid path: {str(e)}"
            }), 400
        
        # Check if file exists
        if not full_pdf_path.exists():
            return jsonify({
                "success": False,
                "error": f"PDF file not found: {pdf_path}"
            }), 404
        
        # Check if it's actually a PDF file
        if not full_pdf_path.suffix.lower() == '.pdf':
            return jsonify({
                "success": False,
                "error": "File is not a PDF"
            }), 400
        
        print(f"\n{'='*80}")
        print(f"Serving PDF file: {full_pdf_path}")
        print(f"{'='*80}\n")
        
        # Extract filename for download
        filename = full_pdf_path.name
        
        # Send file with appropriate headers
        return send_file(
            str(full_pdf_path),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in download_resume: {error_trace}")
        return jsonify({
            "success": False,
            "error": f"Error serving PDF: {str(e)}"
        }), 500


if __name__ == '__main__':
    # Use port 5001 instead of 5000 to avoid conflict with macOS AirPlay Receiver
    port = int(os.getenv('PORT', 5001))
    print(f"Starting API server on http://localhost:{port}")
    app.run(host='localhost', port=port, debug=True)

