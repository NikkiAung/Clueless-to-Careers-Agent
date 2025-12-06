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
Job Title: Intern, Digital Retail Transformation

Job Description:
Apply now »
Intern, Digital Retail Transformation
Date:  Dec 1, 2025
Location:  

Fountain Valley, CA, US, 92708

Job Req ID:  2323

At Hyundai, we’ve rethought our business and created cars that combine performance, quality, design and innovation into a complete package.

 

It’s time you rethink what you expect from an employer.

 

At Hyundai, we understand you're not just building a career – you're building a life. We believe in our people and realize that our success is a direct result of our commitment in offering you great opportunities for your career. If you would enjoy working in a dynamic environment and are looking for a chance to become part of a stellar team of professionals, we invite you to apply online today.

 

Intern, Digital Retail Transformation

The Digital Retail Transformation team is looking for a motivated and tech-savvy intern to help shape the future of how customers buy and experience vehicles — balancing dealer and customer experience, utilizing marketing data and available tools to modernize the automotive retail journey. As part of this team, the intern will support projects that connect online and in-store experiences, improve digital marketing tools, and help bring a seamless customer experience across our dealer network. 

 

Major Responsibilities:

Assist in mapping and analyzing the customer journey.
Support implementation of digital retail tools and dealers/customers requests.
Help collect and interpret data to improve digital sales and lead conversion.
Create presentations and reports for leadership summarizing insights, progress, and recommendations.
Collaborate with cross-functional teams (IT, Marketing, and Sales).
Support training materials and communication for dealership adoption of new digital tools.

 

Additional Notes:

Available for a full-time paid internship in June to August 2026   
Local to Fountain Valley, CA (no relocation or housing will be offered) 
Must be eligible to work up to 40 hours per week
Must be legally authorized to work in the US on a full-time basis during the internship   
Visa sponsorship is not available   
Work hours are 8:00 AM to 5:00 PM (Monday-Friday) 
Compensation: $25.00/Hour

 

Education:

Must be a high school graduate
Currently pursuing a Bachelor’s or Master’s degree in Business, Marketing, Digital Strategy, Information Systems, or related field. 

 

Skills/Knowledge:

Strong interest in the automotive industry, digital innovation, and customer experience.
Proficiency with Microsoft Office / Google Workspace (Excel, PowerPoint, etc.); familiarity with analytics tools (e.g., Tableau, Power BI, Google Analytics) is a plus. 
Excellent communication, analytical, and organizational skills. 
Proactive attitude and willingness to learn in a fast-paced environment. 

 

 

Our Company adheres to the equal employment opportunity guidelines set forth by federal, state and local laws.  The information requested on this form is sought in good faith and will not be used to discriminate against the applicant based on race, religion or creed, color, national origin, ancestry, physical disability, mental disability, medical condition, genetic characteristics, marital status, sex or gender (which includes pregnancy, childbirth, or related circumstances), gender identity, gender expression, age, citizenship, sexual orientation, family care or medical leave status, military and veteran status, political affiliation, or any other characteristic protected by federal, state and local laws.

Apply now »

Responsibilities:
Responsibilities:

Assist in mapping and analyzing the customer journey.
Support implementation of digital retail tools and dealers/customers requests.
Help collect and interpret data to improve digital sales and lead conversion.
Create presentations and reports for leadership summarizing insights, progress, and recommendations.
Collaborate with cross-functional teams (IT, Marketing, and Sales).
Support training materials and communication for dealership adoption of new digital tools.

Education Requirements:
Education:

Must be a high school graduate
Currently pursuing a Bachelor’s or Master’s degree in Business, Marketing, Digital Strategy, Information Systems, or related field. 

 

Skills/Knowledge:

Strong interest in the automotive industry, digital innovation, and customer experience.
Proficiency with Microsoft Office / Google Workspace (Excel, PowerPoint, etc.); familiarity with analytics tools (e.g., Tableau, Power BI, Google Analytics) is a plus. 
Excellent communication, analytical, and organizational skills. 
Proactive attitude and willingness to learn in a fast-paced environment.

Benefits and Compensation:
Compensation: $25.00/Hour

 

Education:

Must be a high school graduate
Currently pursuing a Bachelor’s or Master’s degree in Business, Marketing, Digital Strategy, Information Systems, or related field.
    """
    
    try:
        print(f"Sending prompt: {user_prompt}\n")
        agent_response = send_prompt_to_agent(user_prompt)
        print(f"Agent Response:\n{agent_response}")
    except Exception as e:
        print(f"Error: {e}")
