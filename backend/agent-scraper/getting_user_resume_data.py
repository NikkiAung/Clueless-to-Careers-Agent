"""
Resume data retrieval from Supabase database.

This module provides functions to fetch and convert resume data from the Supabase
parsed_resumes table for a given user_id.
"""
import os
import json
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from backend directory or root directory
backend_dir = Path(__file__).parent.parent  # Go up from agent-scraper to backend
root_dir = backend_dir.parent  # Go up from backend to project root

# Try loading .env from backend directory first, then root directory
env_loaded = False
env_path = None
if (backend_dir / ".env").exists():
    env_path = backend_dir / ".env"
    load_dotenv(env_path)
    env_loaded = True
    print(f"✓ Loaded .env from backend directory: {env_path}")
elif (root_dir / ".env").exists():
    env_path = root_dir / ".env"
    load_dotenv(env_path)
    env_loaded = True
    print(f"✓ Loaded .env from root directory: {env_path}")
else:
    # Try default load_dotenv() which looks in current directory and parent directories
    load_dotenv()
    print("⚠ Using default load_dotenv() - .env file location not explicitly found")

try:
    from supabase import create_client, Client
except ImportError:
    print("Warning: supabase package not installed. Install it with: pip install supabase")
    Client = None


def get_supabase_client() -> Optional[Client]:
    """
    Create and return a Supabase client.
    
    Returns:
        Client: Supabase client instance, or None if credentials are missing
    """
    if Client is None:
        return None
    
    # Ensure environment variables are loaded (in case called from thread)
    # Reload .env to ensure we have the latest values
    backend_dir = Path(__file__).parent.parent
    root_dir = backend_dir.parent
    if (root_dir / ".env").exists():
        load_dotenv(root_dir / ".env", override=False)  # Don't override if already set
    elif (backend_dir / ".env").exists():
        load_dotenv(backend_dir / ".env", override=False)
    
    # Check for Supabase credentials in order of preference
    # IMPORTANT: Use SERVICE_ROLE_KEY for backend to bypass RLS policies
    # Anon key will be blocked by Row Level Security policies
    supabase_url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    supabase_key = (
        os.getenv("SUPABASE_SERVICE_ROLE_KEY") or  # Preferred: bypasses RLS
        os.getenv("SUPABASE_ANON_KEY") or 
        os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")  # Fallback: may be blocked by RLS
    )
    
    # Warn if using anon key (will likely be blocked by RLS)
    if not os.getenv("SUPABASE_SERVICE_ROLE_KEY") and (os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")):
        print("⚠ WARNING: Using anon key instead of service role key.")
        print("  This may be blocked by Row Level Security (RLS) policies.")
        print("  For backend access, use SUPABASE_SERVICE_ROLE_KEY in your .env file.")
        print("  Get it from: Supabase Dashboard → Project Settings → API → service_role key")
    
    # Debug: Check what environment variables are available
    if not supabase_url or not supabase_key:
        print("=" * 80)
        print("ERROR: Supabase credentials not found in environment variables")
        print("=" * 80)
        print("\nDebugging environment variables:")
        print(f"  SUPABASE_URL: {os.getenv('SUPABASE_URL', 'NOT SET')}")
        print(f"  NEXT_PUBLIC_SUPABASE_URL: {os.getenv('NEXT_PUBLIC_SUPABASE_URL', 'NOT SET')}")
        print(f"  SUPABASE_SERVICE_ROLE_KEY: {'SET' if os.getenv('SUPABASE_SERVICE_ROLE_KEY') else 'NOT SET'}")
        print(f"  SUPABASE_ANON_KEY: {'SET' if os.getenv('SUPABASE_ANON_KEY') else 'NOT SET'}")
        print(f"  NEXT_PUBLIC_SUPABASE_ANON_KEY: {'SET' if os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY') else 'NOT SET'}")
        print("\nTo fix this, make sure your .env file contains:")
        print("\n  NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co")
        print("  NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key")
        print("\nOr use:")
        print("\n  SUPABASE_URL=https://your-project.supabase.co")
        print("  SUPABASE_SERVICE_ROLE_KEY=your_service_role_key")
        print("=" * 80)
        return None
    
    print(f"✓ Supabase URL found: {supabase_url[:30]}...")
    print(f"✓ Supabase key found: {supabase_key[:20]}...")
    
    try:
        return create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None


def fetch_resume_from_supabase(user_id: str) -> Optional[dict]:
    """
    Fetch parsed resume data from Supabase for a given user_id.
    
    Args:
        user_id (str): The user's UUID from auth.users table
        
    Returns:
        dict: Parsed resume data from database matching the schema:
            - id: uuid
            - user_id: uuid
            - name: text
            - location: text
            - phone: text
            - emails: jsonb
            - links: jsonb
            - professional_summary: text
            - education: jsonb
            - work_experience: jsonb
            - projects: jsonb
            - skills: jsonb
            - created_at: timestamp
            - updated_at: timestamp
        Returns None if not found or on error
    """
    supabase = get_supabase_client()
    if not supabase:
        return None
    
    try:
        print(f"Querying Supabase for user_id: {user_id}")
        response = supabase.table("parsed_resumes").select("*").eq("user_id", user_id).execute()
        
        print(f"Supabase response status: {response}")
        print(f"Response data: {response.data}")
        print(f"Number of records found: {len(response.data) if response.data else 0}")
        
        if response.data and len(response.data) > 0:
            print(f"✓ Resume found! Returning first record.")
            return response.data[0]
        else:
            print(f"⚠ No resume found for user_id: {user_id}")
            print(f"  - Response data is: {response.data}")
            print(f"  - Checking if user_id exists in database...")
            
            # Try to check if the table is accessible at all
            try:
                test_response = supabase.table("parsed_resumes").select("user_id").limit(5).execute()
                print(f"  - Test query successful. Sample user_ids in table: {[r.get('user_id') for r in (test_response.data or [])]}")
            except Exception as test_e:
                print(f"  - Error testing table access: {test_e}")
                print(f"  - This might be a Row Level Security (RLS) policy issue")
                print(f"  - Make sure you're using SUPABASE_SERVICE_ROLE_KEY (not anon key) to bypass RLS")
            
            return None
    except Exception as e:
        print(f"❌ Error fetching resume from Supabase: {e}")
        import traceback
        traceback.print_exc()
        return None


def convert_parsed_resume_to_text(parsed_resume: dict) -> str:
    """
    Convert parsed resume data from database to resume text format.
    
    This function formats the structured resume data from the database into
    a plain text format suitable for AI processing.
    
    Args:
        parsed_resume (dict): Parsed resume data from database
        
    Returns:
        str: Formatted resume text with sections:
            - Header (name, location, phone, emails, links)
            - Professional Summary
            - Education
            - Work Experience
            - Project Experience
            - Skills
    """
    lines = []
    
    # Header: Name, Location, Phone, Emails, Links
    header_parts = []
    if parsed_resume.get("name"):
        header_parts.append(parsed_resume["name"])
    if parsed_resume.get("location"):
        header_parts.append(parsed_resume["location"])
    if parsed_resume.get("phone"):
        header_parts.append(parsed_resume["phone"])
    
    # Add emails
    emails = parsed_resume.get("emails")
    if emails:
        if isinstance(emails, list):
            header_parts.extend(emails)
        elif isinstance(emails, str):
            try:
                emails_list = json.loads(emails)
                if isinstance(emails_list, list):
                    header_parts.extend(emails_list)
            except:
                header_parts.append(emails)
    
    # Add links
    links = parsed_resume.get("links")
    if links:
        if isinstance(links, dict):
            for key, value in links.items():
                if value:
                    header_parts.append(str(value))
        elif isinstance(links, str):
            try:
                links_dict = json.loads(links)
                if isinstance(links_dict, dict):
                    for key, value in links_dict.items():
                        if value:
                            header_parts.append(str(value))
            except:
                pass
    
    if header_parts:
        lines.append(" | ".join(header_parts))
        lines.append("")
    
    # Professional Summary
    if parsed_resume.get("professional_summary"):
        lines.append("PROFESSIONAL SUMMARY")
        lines.append(parsed_resume["professional_summary"])
        lines.append("")
    
    # Education
    education = parsed_resume.get("education")
    if education:
        lines.append("EDUCATION")
        if isinstance(education, dict):
            # If it's a dict with 'text' key (from our conversion)
            if "text" in education:
                lines.append(education["text"])
            else:
                # Otherwise, format the dict
                lines.append(json.dumps(education, indent=2))
        elif isinstance(education, str):
            try:
                education_dict = json.loads(education)
                if isinstance(education_dict, dict) and "text" in education_dict:
                    lines.append(education_dict["text"])
                else:
                    lines.append(education)
            except:
                lines.append(education)
        lines.append("")
    
    # Work Experience
    work_experience = parsed_resume.get("work_experience")
    if work_experience:
        lines.append("WORK EXPERIENCE")
        if isinstance(work_experience, dict):
            if "text" in work_experience:
                lines.append(work_experience["text"])
            else:
                lines.append(json.dumps(work_experience, indent=2))
        elif isinstance(work_experience, str):
            try:
                work_dict = json.loads(work_experience)
                if isinstance(work_dict, dict) and "text" in work_dict:
                    lines.append(work_dict["text"])
                else:
                    lines.append(work_experience)
            except:
                lines.append(work_experience)
        lines.append("")
    
    # Projects
    projects = parsed_resume.get("projects")
    if projects:
        lines.append("PROJECT EXPERIENCE")
        if isinstance(projects, list):
            for project in projects:
                if isinstance(project, dict):
                    name = project.get("name", "")
                    description = project.get("description", "")
                    technologies = project.get("technologies", [])
                    
                    tech_str = ""
                    if technologies:
                        if isinstance(technologies, list):
                            tech_str = " | ".join(technologies)
                        else:
                            tech_str = str(technologies)
                    
                    if name:
                        if tech_str:
                            lines.append(f"{name}\t{tech_str}")
                        else:
                            lines.append(name)
                    if description:
                        # Add bullet points if description has multiple lines
                        desc_lines = description.split("\n")
                        for desc_line in desc_lines:
                            if desc_line.strip():
                                lines.append(f"●\t{desc_line.strip()}")
                elif isinstance(project, str):
                    lines.append(project)
        elif isinstance(projects, str):
            try:
                projects_list = json.loads(projects)
                if isinstance(projects_list, list):
                    for project in projects_list:
                        if isinstance(project, dict):
                            name = project.get("name", "")
                            description = project.get("description", "")
                            if name:
                                lines.append(name)
                            if description:
                                lines.append(f"●\t{description}")
            except:
                lines.append(projects)
        lines.append("")
    
    # Skills
    skills = parsed_resume.get("skills")
    if skills:
        lines.append("SKILLS")
        if isinstance(skills, dict):
            for category, skill_list in skills.items():
                if skill_list:
                    if isinstance(skill_list, list):
                        skill_str = ", ".join(skill_list)
                        lines.append(f"{category}: {skill_str}")
                    else:
                        lines.append(f"{category}: {skill_list}")
        elif isinstance(skills, str):
            try:
                skills_dict = json.loads(skills)
                if isinstance(skills_dict, dict):
                    for category, skill_list in skills_dict.items():
                        if skill_list:
                            if isinstance(skill_list, list):
                                skill_str = ", ".join(skill_list)
                                lines.append(f"{category}: {skill_str}")
                            else:
                                lines.append(f"{category}: {skill_list}")
            except:
                lines.append(skills)
        lines.append("")
    
    return "\n".join(lines)


def get_user_resume_text(user_id: str) -> Optional[str]:
    """
    Get user resume text from Supabase database.
    
    This is the main function to retrieve and convert resume data for a user.
    It fetches the parsed resume from the database and converts it to text format.
    
    Args:
        user_id (str): The user's UUID from auth.users table
        
    Returns:
        str: Formatted resume text, or None if resume not found or error occurred
    """
    parsed_resume = fetch_resume_from_supabase(user_id)
    if not parsed_resume:
        return None
    
    return convert_parsed_resume_to_text(parsed_resume)
