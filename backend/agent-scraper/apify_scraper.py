import asyncio
import re
from typing import Dict, Optional
from urllib.parse import urlparse
try:
    from crawlee.crawlers import PlaywrightCrawler
    # The context type will be inferred from PlaywrightCrawler
    from typing import Any
    PlaywrightCrawlingContext = Any  # Type alias for the context
except ImportError:
    # Fallback if crawlee is not installed
    print("Warning: crawlee not installed. Please install with: pip install 'crawlee[playwright]'")
    PlaywrightCrawler = None
    PlaywrightCrawlingContext = None
from playwright.async_api import Page


async def scrape_job_posting(url: str) -> Dict[str, str]:
    """
    Scrape job posting information from a given URL.
    
    This function uses Crawlee with Playwright to extract job information
    including title, description, responsibilities, skills, education, etc.
    
    Args:
        url (str): The URL of the job posting to scrape
        
    Returns:
        Dict[str, str]: A dictionary containing extracted job information:
            - job_title: The job title
            - company: Company name
            - location: Job location
            - job_description: Full job description
            - responsibilities: Key responsibilities
            - skills: Required skills and competencies
            - education: Education requirements
            - experience: Experience requirements
            - benefits: Benefits and compensation
            - full_text: Complete scraped text for fallback
    """
    if PlaywrightCrawler is None:
        raise ImportError(
            "Crawlee is not installed. Please install it with: "
            "pip install crawlee[playwright] && playwright install chromium"
        )
    
    # Determine the job site type
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    job_data = {
        "job_title": "",
        "company": "",
        "location": "",
        "job_description": "",
        "responsibilities": "",
        "skills": "",
        "education": "",
        "experience": "",
        "benefits": "",
        "full_text": ""
    }
    
    async def handle_page(context) -> None:
        """Handle the page scraping logic"""
        page: Page = context.page
        
        # Set user agent to avoid detection
        try:
            await page.set_extra_http_headers({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
        except Exception as e:
            print(f"Warning: Could not set user agent: {e}")
        
        # Wait for page to load with multiple strategies
        try:
            await page.wait_for_load_state("networkidle", timeout=30000)
        except Exception as e:
            print(f"Warning: networkidle timeout, trying domcontentloaded: {e}")
            try:
                await page.wait_for_load_state("domcontentloaded", timeout=10000)
            except Exception as e2:
                print(f"Warning: domcontentloaded also timed out: {e2}")
        
        # Additional wait for dynamic content
        await asyncio.sleep(2)
        
        # Get the full page text first (important fallback)
        try:
            full_text = await page.inner_text("body")
            job_data["full_text"] = full_text
            print(f"✓ Extracted full_text length: {len(full_text)} characters")
            
            # Check if we got meaningful content
            if len(full_text) < 100:
                print(f"⚠ Warning: Full text is very short ({len(full_text)} chars). Page might require authentication or have blocking.")
                # Try to get page title as fallback
                try:
                    title = await page.title()
                    print(f"Page title: {title}")
                    if title and len(title) > 10:
                        job_data["full_text"] = f"{title}\n\n{full_text}"
                except:
                    pass
        except Exception as e:
            print(f"❌ Error getting full text: {e}")
            job_data["full_text"] = ""
        
        # Try to extract structured data based on common job site patterns
        if "linkedin.com" in domain:
            await _scrape_linkedin(page, job_data)
        elif "indeed.com" in domain:
            await _scrape_indeed(page, job_data)
        elif "glassdoor.com" in domain:
            await _scrape_glassdoor(page, job_data)
        elif "monster.com" in domain:
            await _scrape_monster(page, job_data)
        elif "ziprecruiter.com" in domain:
            await _scrape_ziprecruiter(page, job_data)
        elif "careerbuilder.com" in domain:
            await _scrape_careerbuilder(page, job_data)
        elif "dice.com" in domain:
            await _scrape_dice(page, job_data)
        elif "angel.co" in domain or "wellfound.com" in domain:
            await _scrape_angellist(page, job_data)
        elif "stackoverflow.com" in domain:
            await _scrape_stackoverflow(page, job_data)
        elif "remoteok.io" in domain:
            await _scrape_remoteok(page, job_data)
        elif "weworkremotely.com" in domain:
            await _scrape_weworkremotely(page, job_data)
        elif "jobs.lever.co" in domain or "lever.co" in domain:
            await _scrape_lever(page, job_data)
        elif "greenhouse.io" in domain:
            await _scrape_greenhouse(page, job_data)
        elif "workday.com" in domain:
            await _scrape_workday(page, job_data)
        elif "careers-americas.hyundai.com" in domain or "hyundai.com" in domain:
            await _scrape_hyundai(page, job_data)
        else:
            # Generic scraping for unknown sites
            await _scrape_generic(page, job_data)
    
    # Create and run the crawler
    crawler = PlaywrightCrawler(
        request_handler=handle_page,
        headless=True,
    )
    
    await crawler.run([url])
    
    return job_data


async def _scrape_linkedin(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape LinkedIn job postings"""
    try:
        # Job title
        title_selector = "h1.job-details-jobs-unified-top-card__job-title, h1.top-card-layout__title"
        job_data["job_title"] = await _safe_get_text(page, title_selector)
        
        # Company
        company_selector = "a.job-details-jobs-unified-top-card__company-name, a.topcard__org-name-link"
        job_data["company"] = await _safe_get_text(page, company_selector)
        
        # Location
        location_selector = "span.job-details-jobs-unified-top-card__bullet, span.topcard__flavor--bullet"
        job_data["location"] = await _safe_get_text(page, location_selector)
        
        # Job description
        desc_selector = "div.job-details-jobs-unified-top-card__job-description, div.show-more-less-html__markup"
        job_data["job_description"] = await _safe_get_text(page, desc_selector)
        
        # Extract sections from description
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities", "what you'll do", "key responsibilities"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements", "skills", "competencies", "what you bring"])
        job_data["education"] = _extract_section(full_desc, ["education", "degree", "bachelor", "master"])
        job_data["experience"] = _extract_section(full_desc, ["experience", "years", "minimum"])
        job_data["benefits"] = _extract_section(full_desc, ["benefits", "compensation", "salary", "perks"])
        
    except Exception as e:
        print(f"Error scraping LinkedIn: {e}")


async def _scrape_indeed(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Indeed job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.jobsearch-JobInfoHeader-title, h2.jobTitle")
        job_data["company"] = await _safe_get_text(page, "a[data-testid='inlineHeader-companyName'], div.companyName")
        job_data["location"] = await _safe_get_text(page, "div[data-testid='job-location'], div.jobLocation")
        job_data["job_description"] = await _safe_get_text(page, "div#jobDescriptionText, div.jobsearch-jobDescriptionText")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities", "duties"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements", "skills"])
        job_data["education"] = _extract_section(full_desc, ["education", "degree"])
        job_data["experience"] = _extract_section(full_desc, ["experience", "years"])
        job_data["benefits"] = _extract_section(full_desc, ["benefits", "compensation"])
    except Exception as e:
        print(f"Error scraping Indeed: {e}")


async def _scrape_glassdoor(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Glassdoor job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h2[data-test='job-title'], h1.jobTitle")
        job_data["company"] = await _safe_get_text(page, "span[data-test='employer-name'], div.employerName")
        job_data["location"] = await _safe_get_text(page, "span[data-test='job-location'], div.location")
        job_data["job_description"] = await _safe_get_text(page, "div.jobDesc, div[data-test='jobDescriptionText']")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities", "what you'll do"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements", "skills"])
        job_data["education"] = _extract_section(full_desc, ["education", "degree"])
        job_data["experience"] = _extract_section(full_desc, ["experience", "years"])
        job_data["benefits"] = _extract_section(full_desc, ["benefits", "compensation"])
    except Exception as e:
        print(f"Error scraping Glassdoor: {e}")


async def _scrape_monster(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Monster job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.title, h1.jobTitle")
        job_data["company"] = await _safe_get_text(page, "div.company, span.company-name")
        job_data["location"] = await _safe_get_text(page, "div.location, span.location")
        job_data["job_description"] = await _safe_get_text(page, "div.job-description, div#JobDescription")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements"])
        job_data["education"] = _extract_section(full_desc, ["education"])
        job_data["experience"] = _extract_section(full_desc, ["experience"])
    except Exception as e:
        print(f"Error scraping Monster: {e}")


async def _scrape_ziprecruiter(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape ZipRecruiter job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.job_title, h1[data-testid='job-title']")
        job_data["company"] = await _safe_get_text(page, "a.company_name, span[data-testid='company-name']")
        job_data["location"] = await _safe_get_text(page, "div.job_location, span[data-testid='job-location']")
        job_data["job_description"] = await _safe_get_text(page, "div.job_description, div[data-testid='job-description']")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements"])
        job_data["education"] = _extract_section(full_desc, ["education"])
    except Exception as e:
        print(f"Error scraping ZipRecruiter: {e}")


async def _scrape_careerbuilder(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape CareerBuilder job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.job-title, h1[data-testid='job-title']")
        job_data["company"] = await _safe_get_text(page, "a.company-name, span.company")
        job_data["location"] = await _safe_get_text(page, "div.location, span.location")
        job_data["job_description"] = await _safe_get_text(page, "div.job-description, div.description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications"])
    except Exception as e:
        print(f"Error scraping CareerBuilder: {e}")


async def _scrape_dice(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Dice job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.jobTitle, h1[data-testid='job-title']")
        job_data["company"] = await _safe_get_text(page, "a.companyName, span.company")
        job_data["location"] = await _safe_get_text(page, "li.location, span.location")
        job_data["job_description"] = await _safe_get_text(page, "div.jobDescription, div.description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["skills"] = _extract_section(full_desc, ["skills", "technologies", "requirements"])
        job_data["experience"] = _extract_section(full_desc, ["experience", "years"])
    except Exception as e:
        print(f"Error scraping Dice: {e}")


async def _scrape_angellist(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape AngelList/Wellfound job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.u-fontSize24, h1.job-title")
        job_data["company"] = await _safe_get_text(page, "a.startup-link, a.company-name")
        job_data["location"] = await _safe_get_text(page, "span.location, div.location")
        job_data["job_description"] = await _safe_get_text(page, "div.job-description, div.description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["skills"] = _extract_section(full_desc, ["requirements", "skills"])
    except Exception as e:
        print(f"Error scraping AngelList: {e}")


async def _scrape_stackoverflow(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Stack Overflow Jobs"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.-title, h1.job-title")
        job_data["company"] = await _safe_get_text(page, "a.-company, a.company-name")
        job_data["location"] = await _safe_get_text(page, "span.-location, span.location")
        job_data["job_description"] = await _safe_get_text(page, "div.description, div.job-description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["skills"] = _extract_section(full_desc, ["requirements", "technologies", "skills"])
    except Exception as e:
        print(f"Error scraping Stack Overflow: {e}")


async def _scrape_remoteok(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape RemoteOK job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.job-title, h1[itemprop='title']")
        job_data["company"] = await _safe_get_text(page, "h2.company, span[itemprop='name']")
        job_data["location"] = await _safe_get_text(page, "span.location, div.location")
        job_data["job_description"] = await _safe_get_text(page, "div.description, div[itemprop='description']")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["skills"] = _extract_section(full_desc, ["requirements", "skills"])
    except Exception as e:
        print(f"Error scraping RemoteOK: {e}")


async def _scrape_weworkremotely(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape We Work Remotely job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.listing-header-title, h1.title")
        job_data["company"] = await _safe_get_text(page, "h2.listing-company-name, h2.company")
        job_data["location"] = await _safe_get_text(page, "span.location, div.location")
        job_data["job_description"] = await _safe_get_text(page, "div.listing-container, div.description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["skills"] = _extract_section(full_desc, ["requirements", "skills"])
    except Exception as e:
        print(f"Error scraping We Work Remotely: {e}")


async def _scrape_lever(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Lever job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h2.posting-headline, h1.posting-title")
        job_data["company"] = await _safe_get_text(page, "a.posting-category-title, span.company")
        job_data["location"] = await _safe_get_text(page, "div.posting-categories, span.location")
        job_data["job_description"] = await _safe_get_text(page, "div.section, div.posting-description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities", "the team", "the role"])
        job_data["skills"] = _extract_section(full_desc, ["requirements", "qualifications", "nice to have"])
    except Exception as e:
        print(f"Error scraping Lever: {e}")


async def _scrape_greenhouse(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Greenhouse job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h1.app-title, h1.job-title")
        job_data["company"] = await _safe_get_text(page, "span.company-name, a.company")
        job_data["location"] = await _safe_get_text(page, "div.location, span.location")
        job_data["job_description"] = await _safe_get_text(page, "div#content, div.description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["the role", "responsibilities"])
        job_data["skills"] = _extract_section(full_desc, ["requirements", "qualifications"])
    except Exception as e:
        print(f"Error scraping Greenhouse: {e}")


async def _scrape_workday(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Workday job postings"""
    try:
        job_data["job_title"] = await _safe_get_text(page, "h2[data-automation-id='jobPostingHeader'], h1.job-title")
        job_data["company"] = await _safe_get_text(page, "a[data-automation-id='jobPostingCompanyName'], span.company")
        job_data["location"] = await _safe_get_text(page, "dd[data-automation-id='jobPostingLocation'], span.location")
        job_data["job_description"] = await _safe_get_text(page, "div[data-automation-id='jobPostingDescription'], div.description")
        
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements"])
    except Exception as e:
        print(f"Error scraping Workday: {e}")


async def _scrape_hyundai(page: Page, job_data: Dict[str, str]) -> None:
    """Scrape Hyundai careers job postings"""
    try:
        # Wait for page to load
        await page.wait_for_load_state("networkidle", timeout=30000)
        
        # Job title - usually in h1 or h2
        job_data["job_title"] = await _safe_get_text(page, "h1, h2.job-title, h1.job-title")
        
        # Company
        job_data["company"] = "Hyundai"
        
        # Location - look for location info
        location_selectors = [
            "span.location",
            "div.location",
            "[data-testid='location']",
            "span:has-text('Location')",
        ]
        for selector in location_selectors:
            text = await _safe_get_text(page, selector)
            if text and "CA" in text or "US" in text:
                job_data["location"] = text
                break
        
        # Job description - main content area
        desc_selectors = [
            "div.job-description",
            "div.description",
            "div[class*='description']",
            "div[class*='job-detail']",
            "main",
            "article",
            "div.content"
        ]
        
        for selector in desc_selectors:
            text = await _safe_get_text(page, selector)
            if text and len(text) > 200:
                job_data["job_description"] = text
                break
        
        # If we didn't get description, use full text
        if not job_data["job_description"]:
            full_text = await page.inner_text("body")
            job_data["full_text"] = full_text
            job_data["job_description"] = full_text
        
        # Extract sections from description
        full_desc = job_data["job_description"] or job_data["full_text"]
        job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities", "major responsibilities", "duties", "what you'll do"])
        job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements", "skills", "skills/knowledge", "competencies"])
        job_data["education"] = _extract_section(full_desc, ["education", "degree", "bachelor", "master", "must be"])
        job_data["experience"] = _extract_section(full_desc, ["experience", "years", "minimum"])
        job_data["benefits"] = _extract_section(full_desc, ["benefits", "compensation", "salary", "perks", "hour"])
        
    except Exception as e:
        print(f"Error scraping Hyundai: {e}")


async def _scrape_generic(page: Page, job_data: Dict[str, str]) -> None:
    """Generic scraping for unknown job sites"""
    try:
        print("Using generic scraper for unknown job site...")
        
        # Try common selectors for job title (more comprehensive)
        title_selectors = [
            "h1",
            "h1.job-title",
            "h1.title",
            "h2.job-title",
            "[data-testid='job-title']",
            "[itemprop='title']",
            ".job-title",
            ".jobTitle",
            "h1[class*='title']",
            "h1[class*='job']"
        ]
        for selector in title_selectors:
            text = await _safe_get_text(page, selector)
            if text and len(text) > 5 and len(text) < 200:
                job_data["job_title"] = text
                print(f"✓ Found job title: {text[:50]}...")
                break
        
        # Try common selectors for company
        company_selectors = [
            "a.company",
            "span.company-name",
            ".company",
            "[data-testid='company-name']",
            "[itemprop='name']",
            ".companyName",
            "a[class*='company']",
            "span[class*='company']"
        ]
        for selector in company_selectors:
            text = await _safe_get_text(page, selector)
            if text and len(text) > 2 and len(text) < 100:
                job_data["company"] = text
                print(f"✓ Found company: {text}")
                break
        
        # Try common selectors for location
        location_selectors = [
            "span.location",
            "div.location",
            ".location",
            "[data-testid='job-location']",
            "[itemprop='address']",
            ".jobLocation"
        ]
        for selector in location_selectors:
            text = await _safe_get_text(page, selector)
            if text and len(text) > 3 and len(text) < 200:
                job_data["location"] = text
                print(f"✓ Found location: {text}")
                break
        
        # Try to find main content area (more comprehensive)
        content_selectors = [
            "div.job-description",
            "div.description",
            "div.content",
            "article",
            "main",
            "div[role='main']",
            "[data-testid='job-description']",
            "[itemprop='description']",
            ".jobDescription",
            ".job-description-text",
            "div[class*='description']",
            "div[class*='content']",
            "section",
            "#job-description",
            ".job-details"
        ]
        
        for selector in content_selectors:
            text = await _safe_get_text(page, selector)
            if text and len(text) > 200:  # Likely the main description
                job_data["job_description"] = text
                print(f"✓ Found job description ({len(text)} chars) using selector: {selector}")
                break
        
        # If we still don't have a description, try to extract from full_text
        if not job_data.get("job_description") and job_data.get("full_text"):
            full_text = job_data["full_text"]
            # Try to find the main content by looking for the longest paragraph
            # Remove common navigation/footer text
            lines = full_text.split('\n')
            meaningful_lines = [line.strip() for line in lines if len(line.strip()) > 50]
            if meaningful_lines:
                # Take the longest meaningful section
                longest_section = max(meaningful_lines, key=len)
                if len(longest_section) > 200:
                    job_data["job_description"] = longest_section
                    print(f"✓ Extracted job description from full_text ({len(longest_section)} chars)")
        
        # Extract sections from full text
        full_desc = job_data["job_description"] or job_data["full_text"]
        if full_desc:
            job_data["responsibilities"] = _extract_section(full_desc, ["responsibilities", "duties", "what you'll do", "key responsibilities"])
            job_data["skills"] = _extract_section(full_desc, ["qualifications", "requirements", "skills", "competencies", "what you bring"])
            job_data["education"] = _extract_section(full_desc, ["education", "degree", "bachelor", "master", "phd"])
            job_data["experience"] = _extract_section(full_desc, ["experience", "years", "minimum", "required experience"])
            job_data["benefits"] = _extract_section(full_desc, ["benefits", "compensation", "salary", "perks", "what we offer"])
            
            # Log what we extracted
            if job_data["responsibilities"]:
                print(f"✓ Extracted responsibilities ({len(job_data['responsibilities'])} chars)")
            if job_data["skills"]:
                print(f"✓ Extracted skills ({len(job_data['skills'])} chars)")
            if job_data["education"]:
                print(f"✓ Extracted education ({len(job_data['education'])} chars)")
            if job_data["experience"]:
                print(f"✓ Extracted experience ({len(job_data['experience'])} chars)")
            if job_data["benefits"]:
                print(f"✓ Extracted benefits ({len(job_data['benefits'])} chars)")
        else:
            print("⚠ No description or full_text available for section extraction")
        
    except Exception as e:
        print(f"❌ Error in generic scraping: {e}")
        import traceback
        traceback.print_exc()


async def _safe_get_text(page: Page, selector: str) -> str:
    """Safely get text from a selector, returning empty string if not found"""
    try:
        element = await page.query_selector(selector)
        if element:
            text = await element.inner_text()
            return text.strip() if text else ""
    except Exception:
        pass
    return ""


def _extract_section(text: str, keywords: list) -> str:
    """
    Extract a section from text based on keywords.
    
    Looks for sections that start with any of the keywords and extracts
    the content until the next major section or end of text.
    """
    if not text:
        return ""
    
    text_lower = text.lower()
    
    # Find the position of any keyword
    positions = []
    for keyword in keywords:
        # Look for keyword followed by colon, newline, or in heading
        patterns = [
            f"{keyword}:",
            f"{keyword}\n",
            f"{keyword}\r",
            f"\n{keyword}:",
            f"\n{keyword}\n",
            f"## {keyword}",
            f"### {keyword}",
        ]
        for pattern in patterns:
            idx = text_lower.find(pattern.lower())
            if idx != -1:
                positions.append((idx, keyword))
                break
    
    if not positions:
        return ""
    
    # Get the earliest position
    positions.sort()
    start_idx = positions[0][0]
    
    # Find the start of the content (after the keyword)
    content_start = start_idx
    for char in text[start_idx:]:
        if char in [':', '\n', '\r']:
            content_start += 1
        else:
            break
    
    # Find the end of the section (next major heading or end)
    section_end = len(text)
    next_sections = ["\n\n", "\n##", "\n###", "\n*", "\n-", "\n1.", "\n2."]
    
    for i in range(content_start, len(text) - 100):
        for section_marker in next_sections:
            if text[i:i+len(section_marker)] == section_marker:
                # Check if it's a new major section (not just a list item)
                if section_marker in ["\n##", "\n###"]:
                    section_end = i
                    break
                elif section_marker in ["\n\n"] and i > content_start + 200:
                    # Only break on double newline if we have substantial content
                    section_end = i
                    break
        
        if section_end < len(text):
            break
    
    extracted = text[content_start:section_end].strip()
    
    # Limit length to avoid too much text
    if len(extracted) > 2000:
        extracted = extracted[:2000] + "..."
    
    return extracted


def format_job_data_for_prompt(job_data: Dict[str, str]) -> str:
    """
    Format scraped job data into a prompt string for the AI agent.
    
    Args:
        job_data: Dictionary containing job information
        
    Returns:
        str: Formatted prompt string
    """
    prompt_parts = []
    
    if job_data.get("job_title"):
        prompt_parts.append(f"Job Title: {job_data['job_title']}")
    
    if job_data.get("company"):
        prompt_parts.append(f"Company: {job_data['company']}")
    
    if job_data.get("location"):
        prompt_parts.append(f"Location: {job_data['location']}")
    
    if job_data.get("job_description"):
        prompt_parts.append(f"\nJob Description:\n{job_data['job_description']}")
    
    if job_data.get("responsibilities"):
        prompt_parts.append(f"\nResponsibilities:\n{job_data['responsibilities']}")
    
    if job_data.get("skills"):
        prompt_parts.append(f"\nRequired Skills and Competencies:\n{job_data['skills']}")
    
    if job_data.get("education"):
        prompt_parts.append(f"\nEducation Requirements:\n{job_data['education']}")
    
    if job_data.get("experience"):
        prompt_parts.append(f"\nExperience Requirements:\n{job_data['experience']}")
    
    if job_data.get("benefits"):
        prompt_parts.append(f"\nBenefits and Compensation:\n{job_data['benefits']}")
    
    # If we don't have structured data, use the full text
    if not any([job_data.get("job_description"), job_data.get("responsibilities"), 
            job_data.get("skills"), job_data.get("education")]):
        if job_data.get("full_text") and len(job_data.get("full_text", "")) > 200:
            prompt_parts.append(f"\nFull Job Posting:\n{job_data['full_text']}")
    
    # If we still have nothing, return empty string (will be handled by caller)
    if len("\n".join(prompt_parts).strip()) < 50:
        return ""
    
    return "\n".join(prompt_parts)


# Main function for testing
async def main():
    """Test the scraper with a sample URL"""
    test_url = input("Enter job posting URL: ").strip()
    if not test_url:
        print("No URL provided")
        return
    
    print(f"Scraping job posting from: {test_url}\n")
    job_data = await scrape_job_posting(test_url)
    
    print("=" * 80)
    print("SCRAPED JOB DATA:")
    print("=" * 80)
    for key, value in job_data.items():
        if value:
            print(f"\n{key.upper()}:")
            print(value[:500] + "..." if len(value) > 500 else value)
    
    print("\n" + "=" * 80)
    print("FORMATTED PROMPT:")
    print("=" * 80)
    formatted = format_job_data_for_prompt(job_data)
    print(formatted)


if __name__ == "__main__":
    asyncio.run(main())
