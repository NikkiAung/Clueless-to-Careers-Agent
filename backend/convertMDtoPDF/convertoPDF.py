"""
Markdown to PDF Converter using weasyprint

This module provides functionality to convert Markdown text to PDF format.
Uses weasyprint which requires system libraries (pango, gdk-pixbuf, gobject).
"""

import os
import sys
from pathlib import Path
from typing import Union

# Set library paths for macOS (needed for weasyprint to find system libraries)
if sys.platform == 'darwin':  # macOS
    homebrew_lib = '/opt/homebrew/lib'
    if os.path.exists(homebrew_lib):
        # Set DYLD_LIBRARY_PATH for dynamic library loading
        current_dyld = os.environ.get('DYLD_LIBRARY_PATH', '')
        if homebrew_lib not in current_dyld:
            os.environ['DYLD_LIBRARY_PATH'] = f"{homebrew_lib}:{current_dyld}" if current_dyld else homebrew_lib
        
        # Set PKG_CONFIG_PATH for pkg-config
        pkg_config_path = '/opt/homebrew/lib/pkgconfig'
        if os.path.exists(pkg_config_path):
            current_pkg = os.environ.get('PKG_CONFIG_PATH', '')
            if pkg_config_path not in current_pkg:
                os.environ['PKG_CONFIG_PATH'] = f"{pkg_config_path}:{current_pkg}" if current_pkg else pkg_config_path

try:
    import markdown
except ImportError:
    markdown = None

# Lazy import for WeasyPrint - only import when actually needed
# This allows the server to start even if WeasyPrint dependencies aren't installed
_weasyprint_available = False
_weasyprint_error = None

def _check_weasyprint():
    """Check if WeasyPrint is available and can be imported."""
    global _weasyprint_available, _weasyprint_error
    if _weasyprint_available:
        return True
    
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
        _weasyprint_available = True
        return True
    except Exception as e:
        _weasyprint_error = str(e)
        return False


def convert_markdown_to_pdf(
    markdown_content: str,
    output_path: Union[str, Path],
) -> str:
    """
    Convert Markdown text to PDF using markdown + weasyprint.

    Args:
        markdown_content: Markdown content as string
        output_path: Path for the output PDF file

    Returns:
        Path to the generated PDF file

    Raises:
        ImportError: If WeasyPrint or its dependencies are not available
        RuntimeError: If conversion fails
    """
    if not markdown_content or not markdown_content.strip():
        raise ValueError("Markdown content cannot be empty")
    
    output_path = Path(output_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Check if markdown is available
    if not markdown:
        raise ImportError("markdown package is not installed. Install it with: pip install markdown")
    
    # Check if WeasyPrint is available (lazy import)
    if not _check_weasyprint():
        error_msg = (
            "WeasyPrint is not available. This is required for PDF conversion.\n\n"
            "To fix this on macOS, install the required system libraries:\n"
            "  brew install pango gdk-pixbuf gobject-introspection\n\n"
            "Then reinstall weasyprint:\n"
            "  pip install --upgrade weasyprint\n\n"
        )
        if _weasyprint_error:
            error_msg += f"Original error: {_weasyprint_error}"
        raise ImportError(error_msg)
    
    # Import WeasyPrint now that we know it's available
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    
    try:
        # Convert markdown to HTML
        html_content = markdown.markdown(
            markdown_content,
            extensions=['extra', 'tables', 'codehilite', 'fenced_code']
        )
        
        # Add basic CSS styling for better PDF appearance
        css_style = """
        @page {
            size: letter;
            margin: 1in;
        }
        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #222;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        h1 { font-size: 24pt; border-bottom: 2px solid #333; padding-bottom: 0.3em; }
        h2 { font-size: 20pt; border-bottom: 1px solid #666; padding-bottom: 0.2em; }
        h3 { font-size: 16pt; }
        h4 { font-size: 14pt; }
        p { margin: 0.5em 0; }
        ul, ol { margin: 0.5em 0; padding-left: 2em; }
        li { margin: 0.3em 0; }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        pre {
            background-color: #f4f4f4;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 1.5em 0;
        }
        """
        
        # Wrap HTML content with proper structure
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>{css_style}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert HTML to PDF using weasyprint
        font_config = FontConfiguration()
        HTML(string=full_html).write_pdf(
            str(output_path),
            font_config=font_config
        )
        
        if not output_path.exists():
            raise RuntimeError(f"PDF file was not created at {output_path}")
        
        print(f"Successfully converted to PDF: {output_path}")
        return str(output_path)
    
    except Exception as e:
        raise RuntimeError(f"Failed to convert markdown to PDF: {str(e)}") from e


def main():
    """Test function - paste your markdown content here."""
    # Paste your markdown content here
    markdown_content = """
**Ye Marn Aung**  
Daly City, CA 94015 • (253) 345‑2360 • jaredaungfr@gmail.com • yaung2@sfsu.edu  
[GitHub](https://github.com/JaredAung) • [LinkedIn](https://www.linkedin.com/in/ye-marn-aung/)  

---  

### Professional Summary  
Analytical Computer Science senior with a strong record of delivering full‑stack, AI‑driven products from data collection through deployment. Proven ability to translate large, unstructured datasets into actionable insights, build interactive dashboards, and communicate findings to diverse stakeholders (engineers, designers, product owners, faculty judges). Skilled in Agile team leadership, cross‑functional collaboration, and modern data‑visualisation tools. Seeking a Business‑Analytics role where technical expertise can drive customer‑journey mapping, lead‑conversion analysis, and digital‑sales performance tracking.  

---  

### Skills  

**Data Analysis & Visualization** – Pandas, NumPy, data cleaning, statistical analysis, exploratory data analysis, Tableau (familiar), Power BI (familiar), Google Analytics (basic), Excel (advanced formulas & pivot tables), Google Sheets, PowerPoint/Google Slides for dashboards and stakeholder decks.  

**Business Tools & Collaboration** – Agile (Scrum), JIRA/Trello, Figma (UX design hand‑off), Microsoft Office, Google Workspace, cross‑functional liaison (IT, Marketing, Sales), stakeholder presentation, demo deck creation.  

**Programming & ML/AI** – Python, Java, JavaScript/TypeScript, SQL, Flask, FastAPI, Next.js, React, Node.js, PyTorch, TensorFlow, Keras, HuggingFace, Scikit‑Learn, OpenCV.  

**Databases & Data Pipelines** – MySQL, PostgreSQL, MongoDB, Pinecone (vector DB), SQL/NoSQL modeling, ETL pipelines, data ingestion & transformation.  

**Cloud & DevOps** – AWS EC2, Docker, Apache 2, Gunicorn, Linux (Ubuntu), Git/GitHub, GitHub Actions, CI/CD.  

---  

### Experience  

**Team Lead / Database Engineer – GaitorGate** (AI‑Powered Search Engine)  
*Flask, MySQL, AWS EC2, Google Gemini, Figma, Git* – **Jan 2024 – May 2024**  

- Directed a 6‑member Agile team; coordinated with UI/UX designers (Figma) and product owner to prioritize features, resulting in the highest‑rated submission among 12 groups.  
- **Collected & cleaned** >10,000 AI‑tool metadata records (JSON/CSV) using Python scripts; stored in MySQL and built automated data‑validation pipelines.  
- Conducted exploratory analysis in **Excel** and **Google Sheets**, generating summary tables that guided keyword‑search algorithm tuning.  
- Crafted a stakeholder demo deck in **Google Slides**, presenting architecture, data flow, and performance metrics to faculty judges and potential users.  
- Developed and maintained secure authentication, NLP‑enhanced search, and a rating/review system; deployed via Apache 2 + Gunicorn on AWS EC2.  

**Developer – MovieCenter** (RAG‑Based Movie Recommender)  
*LangChain, Pinecone, MongoDB, Next.js, Docker, AWS EC2, Pandas* – **Sep 2023 – Dec 2023**  

- Engineered a Retrieval‑Augmented Generation pipeline that ingested **≈10,000** movie records from TMDB API, performed **data cleaning & normalization** with Pandas, and indexed embeddings in Pinecone.  
- Ran statistical analysis (precision@k, recall) in **Jupyter Notebook**; achieved a **30 % lift** in semantic similarity search accuracy over baseline.  
- Produced a **PowerPoint** dashboard summarizing recommendation performance, visualizing hit‑rate trends for product stakeholders.  
- Automated daily data refresh jobs; documented ETL steps in **Google Docs** for cross‑team knowledge sharing.  
- Deployed containerized FastAPI backend on Docker/AWS EC2; integrated with a responsive Next.js/React UI.  

**Developer – Board2Board** (Chess‑Board Recognition AI)  
*Keras, OpenCV, TensorFlow, Jupyter, Git* – **Feb 2023 – May 2023**  

- Designed a computer‑vision pipeline that **collected & labeled** >2,000 chess‑piece images; applied image‑preprocessing and data augmentation to improve model robustness.  
- Conducted **exploratory data analysis** in **Excel** to identify class imbalance and guided oversampling strategy.  
- Trained a fine‑tuned ResNet50 model, attaining **94 % accuracy** across 13 classes; documented results in a visual report using **PowerPoint** for the research symposium.  
- Implemented a linear‑regression‑based adaptive thresholding module, enhancing detection under variable lighting conditions.  

---  

### Projects (Selected)  

| Project | Role | Key Data‑Focused Contributions |
|---------|------|--------------------------------|
| **GaitorGate** | Team Lead / DB Engineer | • Gathered >10k tool records; cleaned and validated schema in MySQL.<br>• Produced Excel pivot‑tables & Google Slides demo deck for judges.<br>• Coordinated with designers (Figma) and product owner to align search features with user needs. |
| **MovieCenter** | Developer | • Extracted & normalized 10k movies via TMDB API; performed statistical analysis with Pandas.<br>• Built PowerPoint performance dashboard for stakeholder review.<br>• Documented pipeline steps in Google Docs for cross‑functional visibility. |
| **Board2Board** | Developer | • Collected 2k+ labeled chess images; used Excel for class‑distribution analysis.<br>• Delivered results in a concise PowerPoint presentation for academic symposium. |

---  

### Education  

**San Francisco State University** – San Francisco, CA  
*Bachelor of Science, Computer Science* (Minor: Mathematics) – Expected Dec 2026  

Relevant Coursework: Data Structures, Database Systems, Machine Learning, Business Analytics Fundamentals, Human‑Computer Interaction.  

---  

### Technical Tools  

- **Languages:** Python, Java, JavaScript/TypeScript, SQL  
- **Web/Cloud:** Flask, FastAPI, Next.js, React, Node.js, AWS EC2, Docker, Apache 2, Gunicorn  
- **Data/ML:** Pandas, NumPy, Scikit‑Learn, TensorFlow/Keras, PyTorch, HuggingFace, OpenCV, LangChain, Pinecone  
- **DB:** MySQL, PostgreSQL, MongoDB, Pinecone (vector)  
- **Visualization/Reporting:** Excel, Google Sheets, PowerPoint, Google Slides, Tableau (familiar), Power BI (familiar)  
- **Collaboration:** Git/GitHub, GitHub Actions, JIRA, Trello, Figma, Google Workspace, Microsoft Office  

---  

*Ready to leverage data‑driven insights, visualization expertise, and cross‑functional collaboration to optimize customer journeys and digital sales performance.*
"""
    
    # Set the output PDF file path
    output_path = "output.pdf"
    
    # Convert to PDF
    convert_markdown_to_pdf(markdown_content, output_path)


if __name__ == "__main__":
    main()
