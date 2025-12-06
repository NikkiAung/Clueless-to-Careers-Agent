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

Aung Nanda Oo
(628) 888-9496 anandaoo.it@gmail.com linkedin.com/in/aung-nanda-oo github.com/NikkiAung
Education
City College Of San Francisco | willing to relocate for jobs Bachelor of Science in Computer Science — GPA - 4.0 Expected Graduation: May 2027
San Francisco, CA
• Dean’s list 2x, Microsoft x Last Mile Education Fund Scholar, 200+ Data Structures and Algorithms Solved Pfp
Technical Skills
Languages: Go, Kotlin, Python, C#, Java, JavaScript, TypeScript, MySQL, GraphQL, PostgreSQL
Developer Tools: AWS, Git, Gitlab, Kubernetes, Docker, Postman, Google Cloud Platform, GNU Linux, HTML5, CSS
Libraries/Frameworks: Angular, MongoDB, ExpressJS, ReactJS, NodeJS, NextJS, Spring Boot, Zustand, Electron
Technical Communication: Tutor my cousin in Scratch, Python, HTML, & CSS, TA for 70+ students in Java and OOP
Work Experience
CCSF Computer Science Department | Released Product Feb 2025 – Jun 2025
Lead Full Stack Software Engineer Intern San Francisco, CA
• Designed desktop app using Electron, React v16+, Node-Cron, JavaScript & Shell scripts enabling 20+
tutors to automate Zoom session scheduling & notifications, improving session delay by 99.9%
• Developed a RESTful API in Node.js with MongoDB (NoSQL) to enable tutors to manage main and overtime
scheduling through CRUD operations in an MVC architecture
• Deployed backend on AWS EC2 using VPC networking (subnets, route tables, NAT, security groups) to ensure
secure API access and protection from external threats
Meta Jun 2025 – Sep 2025
Site Reliable Engineer Intern California, United States
• Managed deployment using Docker for the Flask application, MySQL database, and Nginx reverse proxy on a
CentOS-based Linux VPS, ensuring 99% high uptime and scalability in Scrum rituals
• Automated testing and deployment pipelines using CI/CD, performing regular system health checks and debugging
with Bash+Python scripts, accelerating deployment processes by 50% & reducing production bugs by 30%
• Reduced latency by 30% for high-throughput production traffic via auto-scaling AWS EC2 instances, supporting
100,000 concurrent users via Redis caching and optimized HTTP protocols
• Implemented Prometheus and Grafana monitoring, alerting & visualizing, improving issue detection speed by 40%
CodeDay Labs Jun 2025 – Aug 2025
Lead Open Source Software Engineer Intern | Pull Request : #2261 , #30979, #3299 | Blog Post Remote, United States
• Collaborated with engineers from Dagster company with 50K+ users, using React, TypeScript, GraphQL, & Agile
methodology, enabling direct partition view access from materialized bar, improving UI/UX navigation by 50%
• Contributed to 2.5M+ users Eclipse IDE (Java) by integrating a global keybinding for seamless navigation
through search results, leveraging OOP concepts and implementing 15+ unit and integration tests
A Bank Jun 2023 – Aug 2023
Backend Developer Intern Yangon, Myanmar (Burma)
• Developed 7+ microservices in Java Spring Boot for core banking validity and duplicate checks, integrating JUnit
tests and designing RESTful APIs with Swagger UI to streamline backend–frontend collaboration
• Containerized and deployed banking microservices on AWS (EC2, RDS) using Docker, Kubernetes, Terraform,
and CloudWatch, enabling auto-scaling, real-time payments, and 99.99% uptime for high-traffic operations
• Migrated a code base from a legacy framework to Angular and ReactNative, reducing latency by 2 seconds
Projects
TikTok AI Hackathon Winner | Devpost Next.js | AuthJS | GCP | TypeScript | PostgreSQL | ShadCN
∗ Built AI-powered GitHub repository mentor to help fresh intern with large code base, leading front-end development
using Next.js, TypeScript, Zustand, PostgreSQL, & ShadCN while collaborating with two backend AI engineers
∗ Implemented a full-featured authentication system with email/password login, 2FA OTP code, email verification, forgot
password, social login (GCP Google & GitHub), and secure session management, leveraging AuthJS
Enterprise Travel Assistant AI Agent | Source Code MongoDB | Voyage AI | MCP | Fireworks AI | LangChain
∗ Built AI-powered enterprise travel assistant using MongoDB Atlas, FastAPI, and Next.js (TypeScript) with
LangChain, Fireworks AI (LLM), & Voyage AI embeddings, enabling RAG, context-aware travel planning
∗ Developed an autonomous agent layer leveraging LLM-driven intent detection and semantic retrieval to
dynamically invoke MCP travel tools (flights, hotels, and policies) for real-time, intelligent response

Please format this resume in a professional, clean, and well-structured format.
    """
    
    try:
        print(f"Sending prompt: {user_prompt}\n")
        formatted_resume = format_resume_with_agent(user_prompt)
        print(f"Formatted Resume:\n{formatted_resume}")
    except Exception as e:
        print(f"Error: {e}")

