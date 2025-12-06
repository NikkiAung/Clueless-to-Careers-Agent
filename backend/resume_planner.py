import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def send_prompt_to_agent(prompt: str):
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
    agent_endpoint = os.getenv("DIGITALOCEAN_AGENT_ENDPOINT")
    agent_access_key = os.getenv("DIGITALOCEAN_AGENT_ACCESS_KEY")
    
    if not agent_endpoint or not agent_access_key:
        raise ValueError(
            "Missing required environment variables. "
            "Please ensure DIGITALOCEAN_AGENT_ENDPOINT and "
            "DIGITALOCEAN_AGENT_ACCESS_KEY are set in your .env file."
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
About the job
At Stoke, we believe that a thriving space economy leads to a vibrant, sustainable, and equitable future here on Earth. That is why we are building our fully and rapidly reusable vehicle, Nova. It is designed to fly daily and solve the core challenges of space transportation – it reduces cost, increases availability, and enhances reliability. By radically lowering the cost and increasing the cadence of launch, we’re able to create a truly scalable space industry.

Our team is mission-driven, collaborative, and empowered with ownership of their work. If you want to work with some of the most dedicated and talented people on Earth, come join us.

Description

We know that at the heart of every great challenge is an extraordinary team. Stoke is building a world-class team and we are excited to begin offering internship opportunities for the Spring of 2026. As an intern, you will work on real, open-ended problems that directly contribute to the success of the company. You will work closely with your mentor and other employees who will help you apply your knowledge and grow your skills through high-impact projects. You must be ready to stay focused, move fast, self-direct, and learn on the fly.

Please note: this role requires you to work onsite at our Kent location.

Qualifications

Pursuing Bachelor’s or Master’s degree in mechanical engineering, aerospace engineering, electrical engineering, computer engineering, computer science or a similar STEM field
Project-level experience with Python, C, or Rust
Exceptional command of engineering fundamentals
Hands-on engineering experience through internships, personal projects, work, or teams
Ability to manage a complex technical project and take it through execution
Ability to learn and apply state of the art techniques to technical projects
Excellent written and verbal communication
Able to work full-time, onsite for a minimum of 10-12 consecutive weeks 


Benefits & Opportunities: 

32 hours of paid time off 
On-site gym (Kent, WA location) 
Complimentary snacks & refreshments available on-site 
Company events with Leadership team 
Mentorship from industry-leading engineers 
Direct ownership of real rocket products 


Compensation

Freshman/Sophomore: $28.00/hour
Junior/Senior: $33.00/hour
Completed Bachelor's: $35.00/hour
Completed Master's: $40.00/hour


Applications will be accepted until December 15, 2025. Please note that we will be reviewing applications as they come in, and our slots may get filled before this date.

ITAR Requirements

To conform to U.S. Government space technology export regulations, including the International Traffic in Arms Regulations (ITAR), you must be a U.S. citizen, lawful permanent resident of the U.S., protected individual as defined by 8 U.S.C. 1324b(a)(3), or eligible to obtain the required authorizations from the U.S. Department of State.

Equal Opportunity 

The Company is an Equal Opportunity Employer, including with respect to disability and veteran status. It is committed to compliance with all equal opportunity laws, including the Immigration and Nationality Act (INA) and Title VII. It does not discriminate on the basis of nationality, race, citizenship, immigration status, or any other protected class when it comes to employment practices, including hiring.

Employment at the Company is contingent upon satisfactory completion of reference and background checks, and on your ability to prove your identity and authorization to work in the U.S. for the Company. Employees must comply with the United States Citizenship and Immigration Services employment verification requirements, and, therefore, they must complete an Employment Eligibility Verification Form I-9 at the start of employment and re-verify authorization to work periodically.

Separate from this I-9 process, this position entails access to certain technology and technical data that is restricted under U.S. export control laws and regulations. Employment or continued employment may be conditioned on your legal authorization to work with or have access to export control materials as necessary to perform your job.

E-Verify

Stoke Space uses E-Verify to confirm the identity and employment eligibility of all new hires.
    """
    
    try:
        print(f"Sending prompt: {user_prompt}\n")
        agent_response = send_prompt_to_agent(user_prompt)
        print(f"Agent Response:\n{agent_response}")
    except Exception as e:
        print(f"Error: {e}")
