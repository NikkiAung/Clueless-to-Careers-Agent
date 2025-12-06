import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# TAILOR USER RESUME TO JOB POSTING
# PROMPT: Improvements, Resume
# OUTPUT: Rewritten Resume
def rewrite_resume_with_agent(prompt: str):
    """
    Send a prompt to your Digital Ocean Gradient AI agent and receive a response.
    
    Since you already have an agent configured in Digital Ocean, this function
    connects to your agent endpoint, sends your prompt, and returns the response.
    
    Args:
        prompt (str): The message/prompt you want to send to the agent
        
    Returns:
        str: The response from the agent
    """
    # Load environment variables
    agent_endpoint = os.getenv("TAILOR_RESUME_ENDPOINT")
    # Try to get a specific access key for rewrite resume, otherwise fall back to general one
    agent_access_key = os.getenv("TAILOR_RESUME_ACCESS_KEY") or os.getenv("DIGITALOCEAN_AGENT_ACCESS_KEY")
    
    if not agent_endpoint or not agent_access_key:
        raise ValueError(
            "Missing required environment variables. "
            "Please ensure TAILOR_RESUME_ENDPOINT and "
            "(TAILOR_RESUME_ACCESS_KEY or DIGITALOCEAN_AGENT_ACCESS_KEY) are set in your .env file."
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
improvements: {
  "improvements": [
    {
      "requirement": "Design and implementation of responsive UI components with TypeScript and React based on Figma specs",
      "issue": "weak",
      "suggested_resume_change": "Add a bullet under MovieCenter (or a new front‑end focused project) that explicitly states you translated Figma mockups into responsive React components using TypeScript, mentioning any CSS framework or styling approach used.",
      "section_to_modify": "projects"
    },
    {
      "requirement": "Unit and integration testing of front‑end code",
      "issue": "missing",
      "suggested_resume_change": "If you wrote tests (e.g., Jest, React Testing Library), add a brief line such as “Created unit and integration tests for React components, achieving X% coverage” under the relevant project or experience.",
      "section_to_modify": "experience"
    },
    {
      "requirement": "Contribution to CI/CD pipelines (automated builds, tests, deployments)",
      "issue": "unclear",
      "suggested_resume_change": "Explicitly reference GitHub Actions (or any CI tool) as part of your deployment workflow, e.g., “Configured GitHub Actions to automatically build, test, and deploy the React/Node.js application on each push.”",
      "section_to_modify": "experience"
    },
    {
      "requirement": "Collaboration with product managers / design teams",
      "issue": "weak",
      "suggested_resume_change": "Add a phrase that illustrates cross‑functional collaboration, for example “Worked closely with product managers and UI/UX designers to refine feature requirements and iterate on UI designs.”",
      "section_to_modify": "experience"
    },
    {
      "requirement": "Security considerations in front‑end development (e.g., secure authentication, data handling)",
      "issue": "missing",
      "suggested_resume_change": "If you implemented authentication or safeguarded data, add a concise bullet such as “Implemented secure JWT authentication on the front‑end, ensuring safe data transmission.”",
      "section_to_modify": "experience"
    },
    {
      "requirement": "Open‑source contributions or multi‑person academic projects",
      "issue": "missing",
      "suggested_resume_change": "If you have any public GitHub contributions beyond coursework, list them (e.g., “Contributed bug fixes to XYZ open‑source React component library”) or create a separate “Open‑Source Contributions” line.",
      "section_to_modify": "projects"
    }
  ],
  "reinforce": [
    {
      "requirement": "Proficiency with TypeScript, React, and Node.js",
      "current_evidence": "MovieCenter project lists React, TypeScript, Next.js and Node.js; Additional Skills section lists Node.js, React, TypeScript.",
      "why_reinforce": "Core technical stack for the internship; showcasing depth will strengthen fit.",
      "suggested_resume_change": "Move the React/TypeScript/Node.js bullet to the top of the Projects section and quantify impact (e.g., number of users, performance gains)."
    },
    {
      "requirement": "AI/ML concepts embedded in front‑end features",
      "current_evidence": "GaitorGate includes an AI chatbot (Google Gemini) integrated into UI; MovieCenter uses Gemini for recommendation logic displayed on the front‑end.",
      "why_reinforce": "Matches the job’s emphasis on AI‑enhanced user interactions.",
      "suggested_resume_change": "Add a line highlighting “AI‑driven UI enhancements such as real‑time suggestions and chatbot assistance” under the relevant projects."
    },
    {
      "requirement": "Agile development and team leadership",
      "current_evidence": "Led a 6‑member team using Agile practices for GaitorGate; described as Team Lead, Database Engineer.",
      "why_reinforce": "Demonstrates ability to work in fast‑paced, iterative environments similar to UiPath’s sprints.",
      "suggested_resume_change": "Place the Agile/team‑lead experience earlier in the Experience section and specify sprint cadence (e.g., two‑week sprints)."
    },
    {
      "requirement": "Use of Figma for UI design and hand‑off",
      "current_evidence": "GaitorGate project lists Figma among tools used.",
      "why_reinforce": "Directly aligns with the requirement to translate Figma designs into code.",
      "suggested_resume_change": "Clarify the role of Figma, e.g., “Converted Figma mockups into responsive React components.”"
    },
    {
      "requirement": "Version control and CI tooling (Git, GitHub Actions)",
      "current_evidence": "Additional Skills includes Git/GitHub and GitHub Actions.",
      "why_reinforce": "Shows familiarity with essential development workflows.",
      "suggested_resume_change": "Add a concise bullet such as “Managed source control with Git and automated builds via GitHub Actions.”"
    }
  ],
  "hard_gaps": [
    {
      "requirement": "Explicit front‑end security testing (e.g., OWASP, XSS mitigation)",
      "reason": "Cannot be added without fabrication; resume does not mention security testing."
    },
    {
      "requirement": "Formal code‑review process participation",
      "reason": "No evidence of structured code‑review activities; adding would require inventing experience."
    },
    {
      "requirement": "Quantified performance/scalability metrics for front‑end (load times, bundle size reductions)",
      "reason": "Resume lacks measurable front‑end performance data; cannot be fabricated."
    },
    {
      "requirement": "Open‑source contributions (public pull requests, maintained repos)",
      "reason": "No open‑source activity shown; cannot claim without real contributions."
    }
  ]
}

resume: Ye Marn Aung
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
    
    try:
        print(f"Sending prompt: {user_prompt}\n")
        agent_response = rewrite_resume_with_agent(user_prompt)
        print(f"Agent Response:\n{agent_response}")
    except Exception as e:
        print(f"Error: {e}")

