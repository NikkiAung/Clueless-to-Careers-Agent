# Clueless to Careers Agent: My Journey Building an AI-Powered Career Companion

## What Inspired Me

As a computer science student navigating the competitive job market, I found myself spending countless hours tailoring my resume for each job application. The process was tedious, time-consuming, and often left me wondering if I was highlighting the right skills and experiences. I realized that many job seekers face the same challenge—we're "clueless" about what employers really want to see.

This frustration sparked an idea: **What if AI could help us understand job requirements and automatically tailor our resumes to match them?** I envisioned a system that would:

- Scrape job postings from multiple platforms (LinkedIn, Indeed, Glassdoor, etc.)
- Analyze job requirements using AI
- Intelligently tailor resumes to highlight relevant skills and experiences
- Provide a seamless experience through a Chrome extension

The name "Clueless to Careers Agent" reflects this journey—transforming uncertainty into clarity and action.

## What I Learned

Building this project was a comprehensive learning experience that pushed me beyond my comfort zone:

### **Full-Stack Development**
- **Frontend**: Built a modern Next.js application with TypeScript, React, and Tailwind CSS, implementing authentication flows, protected routes, and responsive design
- **Backend**: Created a Flask API server handling job scraping, AI integration, and resume processing
- **Chrome Extension Development**: Learned Manifest V3 APIs, content scripts, background workers, and the complexities of iframe embedding in extension sidebars

### **Web Scraping & Data Processing**
- Mastered Playwright for dynamic content scraping across 15+ job platforms
- Implemented robust error handling for varying website structures
- Learned to extract structured data from unstructured HTML using CSS selectors and XPath

### **AI Integration**
- Integrated with DigitalOcean's Gradient AI platform for resume tailoring
- Designed effective prompts that guide AI to analyze job requirements and suggest resume improvements
- Implemented a two-stage AI pipeline: first analyzing job-resume gaps, then generating tailored content

### **Chrome Extension Security & Policies**
- Deep dive into Content Security Policy (CSP) and how it affects iframe embedding
- Learned to use `declarativeNetRequest` API to bypass iframe restrictions
- Solved complex issues with form submissions in sandboxed iframes
- Understood the nuances of cross-origin communication using postMessage

### **Database Design & Authentication**
- Set up Supabase for user authentication and data storage
- Designed database schemas for user profiles, job applications, and parsed resumes
- Implemented server-side and client-side authentication flows with Next.js middleware

### **DevOps & Deployment**
- Configured environment variables and secrets management
- Set up CORS policies for local development
- Learned about port conflicts (especially macOS AirPlay on port 5000!)

## How I Built It

The project is architected as a three-tier system:

### **1. Chrome Extension (Frontend Layer)**
The extension provides quick access to the platform directly from the browser:

- **Side Panel**: Embedded iframe displaying the Next.js web app
- **Content Scripts**: Intercept job posting pages and extract URLs
- **Background Worker**: Handles API communication and message passing
- **Popup Interface**: Quick authentication and job application trigger

**Key Technical Challenge**: Getting the Next.js app to work seamlessly in an iframe within a Chrome extension required:
- Configuring CSP headers in `manifest.json`
- Using `declarativeNetRequest` to remove `x-frame-options` headers
- Implementing postMessage communication for navigation
- Handling form submissions in sandboxed iframes

### **2. Next.js Web Application (User Interface)**
A modern, responsive dashboard built with:

- **Authentication**: Supabase Auth with protected routes via middleware
- **Profile Management**: Upload and parse resumes, manage user information
- **Job Tracking**: Track applications, interviews, and offers
- **Resume Builder**: Interface to view and download tailored resumes

**Architecture Highlights**:
- Server-side rendering with Next.js App Router
- Client-side state management with React hooks
- Real-time updates using Supabase subscriptions
- Beautiful UI with Framer Motion animations

### **3. Flask Backend API (Processing Layer)**
The backend orchestrates the entire workflow:

```python
# Simplified workflow
1. Receive job URL from extension
2. Scrape job posting (Playwright)
3. Extract structured data (title, requirements, skills, etc.)
4. Format prompt for AI agent
5. Send to DigitalOcean Gradient AI
6. Process AI response (resume improvements)
7. Return tailored resume to user
```

**Key Components**:
- **Job Scraper Service**: Multi-site scraping with fallback strategies
- **Resume Parser**: Extract skills, experience, and projects from PDFs
- **AI Integration**: Two-stage prompting for gap analysis and content generation
- **PDF Generation**: Convert tailored resumes to downloadable PDFs

### **Technology Stack**

| Layer | Technologies |
|-------|-------------|
| **Extension** | Chrome Extension Manifest V3, JavaScript, HTML/CSS |
| **Frontend** | Next.js 14, TypeScript, React, Tailwind CSS, Framer Motion |
| **Backend** | Flask, Python, Playwright, PyPDF2 |
| **AI/ML** | DigitalOcean Gradient AI, Custom prompt engineering |
| **Database** | Supabase (PostgreSQL), Row Level Security |
| **Authentication** | Supabase Auth, JWT tokens |
| **Deployment** | Local development (Vercel-ready for frontend) |

## Challenges I Faced

### **1. Chrome Extension Iframe Restrictions**
**Problem**: The Next.js app worked perfectly in a regular browser but failed when embedded in the Chrome extension sidebar. Form submissions wouldn't trigger, and navigation was blocked.

**Solution**: 
- Added explicit CSP policies in `manifest.json` allowing form actions
- Used `declarativeNetRequest` to remove restrictive headers (`x-frame-options`, `content-security-policy`)
- Implemented postMessage communication between iframe and extension
- Added `allow-top-navigation` to iframe sandbox attributes
- Created fallback navigation using `window.location.href` when router.push() failed

**Learning**: Chrome extensions have strict security policies that require careful configuration. The `sandbox` attribute and CSP are powerful but can be restrictive if not properly configured.

### **2. Multi-Site Web Scraping**
**Problem**: Each job platform has different HTML structures, dynamic content loading, and anti-scraping measures. A single scraping strategy wouldn't work.

**Solution**:
- Created site-specific scrapers for LinkedIn, Indeed, Glassdoor, etc.
- Implemented a generic fallback scraper using Playwright's content extraction
- Added retry logic and error handling for network issues
- Used CSS selectors and XPath with fallback strategies
- Implemented structured data extraction with validation

**Learning**: Web scraping requires flexibility and robust error handling. Always have fallback strategies and validate extracted data.

### **3. AI Prompt Engineering**
**Problem**: Getting the AI to provide actionable, structured resume improvements was challenging. Initial prompts produced generic or irrelevant suggestions.

**Solution**:
- Designed a two-stage approach:
  1. **Analysis Stage**: AI identifies gaps between job requirements and current resume
  2. **Generation Stage**: AI suggests specific improvements with examples
- Created detailed prompt templates with examples
- Implemented JSON-structured responses for easier parsing
- Added validation to ensure AI responses meet quality standards

**Learning**: Effective AI prompting requires clear structure, examples, and iterative refinement. The quality of output directly correlates with prompt quality.

### **4. Resume Parsing Accuracy**
**Problem**: Extracting structured data from PDF resumes is notoriously difficult due to varying formats, layouts, and styles.

**Solution**:
- Used PyPDF2 for text extraction
- Implemented regex patterns for common resume sections
- Created a fallback manual parsing interface
- Stored parsed data in Supabase for future use
- Allowed users to edit and correct parsed information

**Learning**: PDF parsing is an imperfect science. Providing user feedback and correction mechanisms is essential.

### **5. State Management Across Extension and Web App**
**Problem**: Keeping authentication state synchronized between the Chrome extension and the embedded web app was complex.

**Solution**:
- Used Supabase's client-side SDK in both contexts
- Implemented shared authentication via Supabase session tokens
- Created middleware to protect routes and handle redirects
- Used localStorage for extension state persistence

**Learning**: Cross-context state management requires careful design. Using a shared authentication provider (Supabase) simplified this significantly.

### **6. Port Conflicts and CORS Issues**
**Problem**: macOS uses port 5000 for AirPlay Receiver, causing conflicts. CORS policies blocked API requests from the extension.

**Solution**:
- Changed default backend port to 5001
- Configured Flask-CORS to allow extension origins
- Added environment variable configuration for flexible port assignment
- Documented port requirements clearly

**Learning**: Always check for port conflicts, especially on macOS. CORS configuration is crucial for extension-to-backend communication.

## Impact & Future Vision

This project has been a transformative learning experience. It taught me:

- **System Design**: How to architect a complex, multi-component system
- **Problem-Solving**: Debugging issues across different layers (extension, frontend, backend)
- **User Experience**: Balancing functionality with ease of use
- **AI Integration**: Practical applications of AI in real-world scenarios

### **Future Enhancements**

1. **Enhanced AI Capabilities**: Fine-tune models specifically for resume tailoring
2. **Cover Letter Generation**: Automatically generate tailored cover letters
3. **Interview Preparation**: AI-powered interview question generation based on job requirements
4. **Analytics Dashboard**: Track application success rates and identify improvement areas
5. **Multi-language Support**: Support for resumes and job postings in multiple languages
6. **Chrome Web Store**: Publish the extension for public use

## Conclusion

Building "Clueless to Careers Agent" was more than just a project—it was a journey from frustration to innovation. It combined my passion for AI, web development, and solving real-world problems. The challenges I faced taught me resilience, the importance of thorough testing, and the value of understanding system-level constraints.

Most importantly, it reinforced my belief that technology should make life easier. By automating the tedious process of resume tailoring, I hope to help job seekers focus on what matters most: showcasing their unique value and landing their dream careers.

---

*Built with ❤️ using Next.js, Flask, Playwright, and DigitalOcean Gradient AI*

