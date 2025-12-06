import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def ask_agent_for_improvements(prompt: str):
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
    agent_endpoint = os.getenv("USER_JOB_MATCH_ENDPOINT")
    # Try to get a specific access key for user job match, otherwise fall back to general one
    agent_access_key = os.getenv("USER_JOB_MATCH_ACCESS_KEY") 
    
    if not agent_endpoint or not agent_access_key:
        raise ValueError(
            "Missing required environment variables. "
            "Please ensure USER_JOB_MATCH_ENDPOINT and "
            "(USER_JOB_MATCH_ACCESS_KEY or DIGITALOCEAN_AGENT_ACCESS_KEY) are set in your .env file."
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
Insights: ```json
{
  "job_meta": {
    "job_title": "Front-End Software Engineer Intern",
    "company": "UiPath",
    "location": "Bellevue, WA",
    "seniority_level": "intern"
  },
  "resume_outline": {
    "target_title": "Front-End Software Engineer Intern",
    "sections": [
      {
        "name": "Summary",
        "sentences": [
          "Passionate computer science student with strong fundamentals and hands‑on experience building modern web applications using TypeScript, React, and Node.js.",
          "Demonstrated ability to translate product requirements into high‑performance, secure, and scalable front‑end solutions while collaborating closely with product managers and design teams.",
          "Experience integrating AI/ML concepts into UI features and delivering code through CI/CD pipelines in fast‑paced, agile environments."
        ]
      },
      {
        "name": "Skills",
        "groups": [
          {
            "label": "Programming Languages & Frameworks",
            "must_include": ["TypeScript", "React", "Node.js"],
            "nice_to_include": []
          },
          {
            "label": "Artificial Intelligence & Machine Learning",
            "must_include": ["AI concepts", "Machine Learning fundamentals"],
            "nice_to_include": []
          },
          {
            "label": "Design & Prototyping Tools",
            "must_include": ["Figma"],
            "nice_to_include": []
          },
          {
            "label": "Tools & Practices",
            "must_include": ["Git", "CI/CD pipelines", "Agile development"],
            "nice_to_include": []
          }
        ]
      },
      {
        "name": "Experience",
        "role_guidelines": [
          {
            "role_hint": "Front-End Software Engineer Intern (or similar internship / project role)",
            "focus_bullets_on": [
              "Designed and implemented responsive UI components with TypeScript and React, adhering to UI/UX specifications from Figma.",
              "Integrated front‑end code with Node.js backend services, ensuring secure data handling and high performance.",
              "Collaborated with product managers and cross‑functional teams to define technical requirements and deliver features iteratively.",
              "Applied AI/ML concepts to enhance user interactions (e.g., predictive suggestions, intelligent automation triggers).",
              "Wrote unit and integration tests; participated in code reviews to maintain quality and security standards.",
              "Contributed to CI/CD pipelines for automated builds, tests, and deployments in an agile sprint cadence.",
              "Documented work and created knowledge‑share materials for teammates.",
              "Participated in open‑source contributions or multi‑person academic projects, showcasing teamwork and code ownership."
            ]
          }
        ],
        "max_total_bullets": 10
      },
      {
        "name": "Projects",
        "project_selection_rules": [
          "Include at least one project that showcases a full‑stack web app built with React, TypeScript, and Node.js.",
          "Include a project where AI/ML concepts were embedded into the front‑end experience (e.g., recommendation engine, chat assistance).",
          "Include a project that used Figma or another design tool for UI mockups and translated those designs into code.",
          "Highlight any project that employed CI/CD automation, Git version control, or agile workflow practices."
        ]
      },
      {
        "name": "Education",
        "notes": [
          "Pursuing Bachelor’s/Master’s/PhD in Computer Science, Mathematics, or a closely related discipline.",
          "Relevant coursework: Data Structures, Algorithms, Operating Systems, Machine Learning, Human‑Computer Interaction."
        ]
      }
    ],
    "keywords_to_weave_in": [
      "front‑end development",
      "TypeScript",
      "React",
      "Node.js",
      "Figma",
      "AI",
      "machine learning",
      "CI/CD",
      "agile",
      "quality",
      "security",
      "scalability",
      "performance",
      "product management",
      "collaboration",
      "internship",
      "open‑source",
      "computer science fundamentals"
    ]
  }
}
Resume: 
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
    
    try:
        print(f"Sending prompt: {user_prompt}\n")
        agent_response = send_prompt_to_agent(user_prompt)
        print(f"Agent Response:\n{agent_response}")
    except Exception as e:
        print(f"Error: {e}")

