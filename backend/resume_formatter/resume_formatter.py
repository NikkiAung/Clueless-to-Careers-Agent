import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# FORMAT RESUME
# PROMPT: Format the resume according to specified guidelines
# OUTPUT: Formatted resume
def format_resume_with_agent(prompt: str):
    """
    Send a prompt to your Digital Ocean Gradient AI agent to format a resume.
    
    Since you already have an agent configured in Digital Ocean, this function
    connects to your agent endpoint, sends your prompt, and returns the formatted resume.
    
    Args:
        prompt (str): The message/prompt you want to send to the agent (typically includes resume and formatting instructions)
        
    Returns:
        str: The formatted resume from the agent
    """
    # Load environment variables
    agent_endpoint = os.getenv("RESUME_FORMATTER_ENDPOINT")
    # Try to get a specific access key for resume formatter, otherwise fall back to general one
    agent_access_key = os.getenv("RESUME_FORMATTER_ACCESS_KEY") or os.getenv("DIGITALOCEAN_AGENT_ACCESS_KEY")
    
    if not agent_endpoint or not agent_access_key:
        raise ValueError(
            "Missing required environment variables. "
            "Please ensure RESUME_FORMATTER_ENDPOINT and "
            "(RESUME_FORMATTER_ACCESS_KEY or DIGITALOCEAN_AGENT_ACCESS_KEY) are set in your .env file."
        )
    
    # Clean up the values (remove quotes if present)
    agent_endpoint = agent_endpoint.strip('"\'')
    agent_access_key = agent_access_key.strip('"\'').strip()
    
    # Prepare the request
    headers = {
        "Authorization": f"Bearer {agent_access_key}",
        "Content-Type": "application/json"
    }
    
    # Agent endpoints use /api/v1/chat/completions path
    # Construct the full URL following Digital Ocean's API format
    if agent_endpoint.endswith("/"):
        chat_url = f"{agent_endpoint}api/v1/chat/completions"
    else:
        chat_url = f"{agent_endpoint}/api/v1/chat/completions"
    
    # Prepare the payload matching the curl command format exactly
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "include_functions_info": False,
        "include_retrieval_info": False,
        "include_guardrails_info": False
    }
    
    # Send the HTTP request to your agent
    try:
        response = requests.post(
            chat_url,
            headers=headers,
            json=payload,
            timeout=60
        )
        
        # Check for errors
        if response.status_code != 200:
            error_detail = response.text
            try:
                error_json = response.json()
                error_detail = error_json.get('error', {}).get('message', error_detail)
            except:
                pass
            raise Exception(f"Agent API request failed (status {response.status_code}): {error_detail}")
        
        # Parse and return the response
        response_data = response.json()
        agent_reply = response_data['choices'][0]['message']['content']
        return agent_reply
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to agent endpoint: {e}")


if __name__ == "__main__":
    # Example usage
    user_prompt = """
Format this resume:

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

Please format this resume in a professional, clean, and well-structured format.
    """
    
    try:
        print(f"Sending prompt: {user_prompt}\n")
        formatted_resume = format_resume_with_agent(user_prompt)
        print(f"Formatted Resume:\n{formatted_resume}")
    except Exception as e:
        print(f"Error: {e}")

