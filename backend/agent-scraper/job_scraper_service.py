"""
Service that integrates job scraping with resume planning.
This module provides a high-level interface for scraping job postings
and sending them to the AI agent for resume tailoring.
"""
import asyncio
import sys
import os
from pathlib import Path

example_resume = """
Ye Marn Aung
Daly City, CA 94015| (253)-345-2360 | jaredaungfr@gmail.com|yaung2@sfsu.edu | https://github.com/JaredAung | https://www.linkedin.com/in/ye-marn-aung/ | 

PROFESSIONAL SUMMARY
Computer Science student at San Francisco State University with hands-on experience delivering full-stack and AI/ML projects from concept to production. Built and deployed applications using various tools for real-world use cases such as AI search engines, RAG-based recommenders, deep-learning networks and computer vision systems. Strong background in cloud deployment, database engineering, and applied AI models development. Seeking opportunities to apply AI and software engineering skills to scalable and user-focused products. 

EDUCATION
San Francisco State University                                                                                              	San Francisco, CA
Bachelor of Science, Computer Science 					       	 Expected December 2026
Minor: Mathematics

PROJECT EXPERIENCE
GaitorGate: AI-Powered Search Engine for AI Applications	          
Team Lead, Database Engineer | Flask, Python, Apache2, Linux Ubuntu, MySQL, AWS EC2, Gunicorn, Google Gemini, Figma, Git 
●	Led a full-stack web application project enabling users to discover AI tools using NLP-enhanced search
●	Integrated secure authentication, NLP and keyword-based searches, a user ratings and review system, AI chatbot (Google Gemini), and deployed and maintained on the AWS EC2 with Apache2 + Gunicorn
●	Applied Agile practices and led a 6-member team to deliver the highest-rated product in a 12 groups competition

MovieCenter: RAG-based LangChain Movie Recommender System	
Developer |LangChain, Python, Pinecone, MongoDB, Google Gemini, Next.js, React, TypeScript, Docker, AWS EC2, FastAPI, Hugging Face SentenceTransformers, TMDB API, Pandas
●	Built a Retrieval-Augmented Generation (RAG) pipeline with LangChain, Pinecone vector DB, MongoDB and Google Gemini to deliver context-rich movie recommendations for close to 10,000 movies 
●	Improved semantic similarity search accuracy by 30% over baseline using HuggingFace SentenceTransformers
●	Deployed a containerized backend with Docker on AWS EC2, and exposed APIs via FastAPI, seamlessly integrated into a Next.js + React frontend

Board2Board: Chess Utility AI for Over-the-Board (OTB) Game Recognition 	
Developer | Keras, Python, OpenCV, ResNet50 Model, Numpy, Scikit-Learn, Linear Regression, Matplotlib, Scipy, Scikit-Image, TensorFlow, Joblib, Jupyter Notebook 
●	Designed a computer vision pipeline with OpenCV to segment chessboard images into 64 cropped square images for piece recognition
●	Fine-tuned a ResNet50 model on a custom hand-labeled dataset of 2,000+ images, achieving 94% accuracy across 13 classes (pieces and empty square) 
●	Incorporated a Linear Regression-based thresholding system in the computer vision pipeline to adapt to variable lighting and image conditions, improving robustness across diverse board images

Additional SKILLS
Web/Cloud: REST APIs, Node.js, Flask, Next.js, React, AWS (EC2), Docker
Programming Languages: Python, Java, JavaScript, TypeScript, SQL
ML/AI: PyTorch, TensorFlow, Keras, HuggingFace, Scikit-Learn, OpenCV
Databases: MySQL, MongoDB, Postgres, Pinecone	
Tools: Firebase, Linux, Render, Github Actions, Git/GitHub 

"""
# Import from the same directory
from resume_planner import send_prompt_to_agent
from apify_scraper import scrape_job_posting, format_job_data_for_prompt

# Import from parent directory (backend/user_job_match and backend/tailor_resume)
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from user_job_match.user_job_map import ask_agent_for_improvements
from tailor_resume.rewrite_resume import rewrite_resume_with_agent
from convertMDtoPDF.convertoPDF import convert_markdown_to_pdf


async def scrape_and_tailor_resume(job_url: str, resume_text: str = None) -> dict:
    """
    Main function that scrapes a job posting and sends it to the AI agent.
    
    This function:
    1. Scrapes the job posting from the given URL
    2. Formats the scraped data into a prompt
    3. Sends the prompt to the AI agent for resume planning (job insights)
    4. Gets improvement suggestions by matching resume to job posting
    5. Rewrites the resume based on improvements
    6. Returns all the data and responses
    
    Args:
        job_url (str): URL of the job posting to scrape
        resume_text (str, optional): The resume text to use. If not provided, uses example_resume.
        
    Returns:
        dict: Dictionary containing:
            - success (bool): Whether the operation was successful
            - job_data (dict): Scraped job information
            - formatted_prompt (str): The formatted prompt sent to AI
            - ai_response (str): The AI agent's response (job insights)
            - improvements (str): Improvement suggestions from user-job match agent
            - rewritten_resume (str): The rewritten resume (Markdown)
            - pdf_path (str): Path to the generated PDF file
            - error (str): Error message if any
    """
    # Use example_resume as default if no resume_text is provided
    resume = resume_text if resume_text else example_resume
    
    result = {
        "success": False,
        "job_data": {},
        "formatted_prompt": "",
        "ai_response": "",
        "improvements": "",
        "rewritten_resume": "",
        "pdf_path": "",
        "error": ""
    }
    
    try:
        # Step 1: Scrape the job posting
        print(f"\n{'='*80}")
        print(f"STEP 1: Scraping job posting from: {job_url}")
        print(f"{'='*80}")
        job_data = await scrape_job_posting(job_url)
        result["job_data"] = job_data
        
        print(f"\nScraping completed. Extracted data:")
        print(f"  - Job Title: {job_data.get('job_title', 'N/A')}")
        print(f"  - Company: {job_data.get('company', 'N/A')}")
        print(f"  - Location: {job_data.get('location', 'N/A')}")
        print(f"  - Description: {len(job_data.get('job_description', ''))} chars")
        print(f"  - Full Text: {len(job_data.get('full_text', ''))} chars")
        
        # Step 2: Format the scraped data into a prompt
        print(f"\n{'='*80}")
        print(f"STEP 2: Formatting scraped data into prompt")
        print(f"{'='*80}")
        formatted_prompt = format_job_data_for_prompt(job_data)
        result["formatted_prompt"] = formatted_prompt
        print(f"Formatted prompt length: {len(formatted_prompt)} characters")
        print(f"Prompt preview (first 200 chars): {formatted_prompt[:200]}...")
        
        # Check if we got any meaningful data
        has_data = (
            job_data.get("job_title") or 
            job_data.get("job_description") or 
            (job_data.get("full_text") and len(job_data.get("full_text", "")) > 200)
        )
        
        if not has_data:
            result["error"] = "Failed to extract sufficient job information from the URL. The page might require authentication or have a different structure."
            return result
        
        # If we have full_text but no formatted prompt, use full_text
        if not formatted_prompt or len(formatted_prompt.strip()) < 50:
            if job_data.get("full_text") and len(job_data.get("full_text", "")) > 200:
                # Use full_text as the prompt if we have it
                formatted_prompt = f"Job Posting:\n\n{job_data['full_text']}"
                result["formatted_prompt"] = formatted_prompt
            else:
                result["error"] = "Failed to extract sufficient job information from the URL"
                return result
        
        # Step 3: Send to AI agent
        print(f"\n{'='*80}")
        print(f"STEP 3: Sending to AI agent")
        print(f"{'='*80}")
        print("Sending job information to AI agent...")
        ai_response = send_prompt_to_agent(formatted_prompt)
        result["ai_response"] = ai_response
        result["success"] = True
        
        print(f"\n✓ AI Agent Response Received!")
        print(f"Response length: {len(ai_response)} characters")
        print(f"\nAI Response Preview (first 500 chars):")
        print(ai_response)
        
        # Check if response is JSON
        if ai_response.strip().startswith('{') or ai_response.strip().startswith('['):
            print(f"\n✓ Response appears to be JSON format")
        else:
            print(f"\n⚠ Response is not JSON format")
        
        # Step 4: Get improvement suggestions by matching resume to job posting
        print(f"\n{'='*80}")
        print(f"STEP 4: Getting improvement suggestions")
        print(f"{'='*80}")
        try:
            improvements_prompt = f"Resume: {resume} + Job Insights: {ai_response}"
            improvements = ask_agent_for_improvements(improvements_prompt)
            result["improvements"] = improvements
            print(f"\n✓ Improvements Received!")
            print(f"Improvements length: {len(improvements)} characters")
            print(f"\nImprovements Preview (first 500 chars):")
            print(improvements)
        except Exception as e:
            error_msg = f"Failed to get improvements: {str(e)}"
            result["error"] = error_msg
            print(f"\n❌ {error_msg}")
        
        # Step 5: Rewrite resume based on improvements
        print(f"\n{'='*80}")
        print(f"STEP 5: Rewriting resume")
        print(f"{'='*80}")
        try:
            rewritten_resume_prompt = f"Improvements: {result.get('improvements', '')} + Resume: {resume}"
            rewritten_resume = rewrite_resume_with_agent(rewritten_resume_prompt)
            result["rewritten_resume"] = rewritten_resume
            print(f"\n✓ Resume Rewritten!")
            print(f"Rewritten resume length: {len(rewritten_resume)} characters")
            print(f"\nRewritten Resume Preview (first 500 chars):")
            print(rewritten_resume)
        except Exception as e:
            error_msg = f"Failed to rewrite resume: {str(e)}"
            if result["error"]:
                result["error"] += f" | {error_msg}"
            else:
                result["error"] = error_msg
            print(f"\n❌ {error_msg}")
        
        # Step 6: Convert rewritten resume (Markdown) to PDF
        print(f"\n{'='*80}")
        print(f"STEP 6: Converting Markdown to PDF")
        print(f"{'='*80}")
        if result.get("rewritten_resume"):
            try:
                # Generate output PDF path
                # Use job title or company name for filename if available
                job_title = result.get("job_data", {}).get("job_title", "resume")
                company = result.get("job_data", {}).get("company", "")
                
                # Sanitize filename
                safe_job_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
                safe_company = "".join(c for c in company if c.isalnum() or c in (' ', '-', '_')).strip()[:30]
                
                if safe_company:
                    pdf_filename = f"tailored_resume_{safe_job_title}_{safe_company}.pdf"
                else:
                    pdf_filename = f"tailored_resume_{safe_job_title}.pdf"
                
                # Remove spaces and replace with underscores
                pdf_filename = pdf_filename.replace(" ", "_")
                
                # Set output path in the convertMDtoPDF directory
                output_dir = backend_path / "convertMDtoPDF"
                output_dir.mkdir(parents=True, exist_ok=True)
                pdf_path = output_dir / pdf_filename
                
                print(f"Converting Markdown to PDF: {pdf_path}")
                pdf_path_str = convert_markdown_to_pdf(
                    markdown_content=result["rewritten_resume"],
                    output_path=pdf_path
                )
                result["pdf_path"] = pdf_path_str
                print(f"\n✓ PDF Generated Successfully!")
                print(f"PDF saved at: {pdf_path_str}")
            except Exception as e:
                error_msg = f"Failed to convert to PDF: {str(e)}"
                if result["error"]:
                    result["error"] += f" | {error_msg}"
                else:
                    result["error"] = error_msg
                print(f"\n❌ {error_msg}")
                import traceback
                traceback.print_exc()
        else:
            print(f"\n⚠ Skipping PDF conversion: No rewritten resume available")
        
        print(f"\n{'='*80}")
        print("Process completed!")
        print(f"{'='*80}\n")
        return result
        
    except Exception as e:
        result["error"] = str(e)
        print(f"Error: {e}")
        return result


def scrape_and_tailor_resume_sync(job_url: str, resume_text: str = None) -> dict:
    """
    Synchronous wrapper for scrape_and_tailor_resume.
    
    This is useful when calling from non-async contexts (like Flask/FastAPI endpoints).
    
    Args:
        job_url (str): URL of the job posting to scrape
        resume_text (str, optional): The resume text to use. If not provided, uses example_resume.
        
    Returns:
        dict: Same as scrape_and_tailor_resume
    """
    return asyncio.run(scrape_and_tailor_resume(job_url, resume_text))


if __name__ == "__main__":
    """Test the service"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python job_scraper_service.py <job_url>")
        sys.exit(1)
    
    job_url = sys.argv[1]
    result = scrape_and_tailor_resume_sync(job_url)
    

