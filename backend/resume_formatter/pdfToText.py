"""
PDF to Text Extractor using pypdf

This module extracts text from PDF files and formats them using the resume formatter.
"""

import sys
from pathlib import Path
from typing import Union

try:
    from pypdf import PdfReader
except ImportError:
    raise ImportError(
        "pypdf is not installed. Install it with: pip install pypdf"
    )

# Add the backend directory to the path to import resume_formatter
script_dir = Path(__file__).parent.resolve()
backend_dir = script_dir.parent
sys.path.insert(0, str(backend_dir))

try:
    # Try importing from resume_formatter package
    from resume_formatter.resume_formatter import format_resume_with_agent
except ImportError:
    try:
        # Fallback: import directly from the file
        import importlib.util
        resume_formatter_path = backend_dir / "resume_formatter" / "resume_formatter.py"
        if resume_formatter_path.exists():
            spec = importlib.util.spec_from_file_location("resume_formatter", resume_formatter_path)
            resume_formatter_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(resume_formatter_module)
            format_resume_with_agent = resume_formatter_module.format_resume_with_agent
        else:
            format_resume_with_agent = None
    except Exception:
        format_resume_with_agent = None
    
    if format_resume_with_agent is None:
        print("Warning: Could not import format_resume_with_agent. Resume formatting will be skipped.")


def extract_text_from_pdf(pdf_path: Union[str, Path]) -> str:
    """
    Extract text from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a string

    Raises:
        FileNotFoundError: If PDF file doesn't exist
        RuntimeError: If extraction fails
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not pdf_path.suffix.lower() == '.pdf':
        raise ValueError(f"File is not a PDF: {pdf_path}")
    
    try:
        # Read the PDF
        reader = PdfReader(str(pdf_path))
        
        # Extract text from all pages
        text_content = []
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
            except Exception as e:
                print(f"Warning: Could not extract text from page {page_num}: {e}")
                continue
        
        if not text_content:
            raise RuntimeError("No text could be extracted from the PDF. The PDF might be scanned (image-based).")
        
        # Join all pages with page separators
        full_text = "\n\n--- Page Break ---\n\n".join(text_content)
        
        return full_text
    
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}") from e


def main():
    """Test function - specify your PDF file path here."""
    # Get the script's directory and resolve path relative to it
    # This ensures it works regardless of the working directory (e.g., when running from debugger)
    script_dir = Path(__file__).parent.resolve()
    project_root = script_dir.parent.parent  # Go up from backend/convertMDtoPDF/ to project root
    pdf_path = project_root / "AungNanda_Oo_Resume.pdf"  # Change this to your PDF file path
    
    try:
        print(f"Extracting text from: {pdf_path}\n")
        extracted_text = extract_text_from_pdf(pdf_path)
        
        print("=" * 80)
        print("Extracted Text:")
        print("=" * 80)
        print(extracted_text)
        print("=" * 80)
        print(f"\nTotal characters extracted: {len(extracted_text)}")
        
        # Format the resume using the resume formatter
        if format_resume_with_agent:
            print("\n" + "=" * 80)
            print("Formatting Resume with AI Agent...")
            print("=" * 80)
            
            # Create prompt similar to the one in resume_formatter.py's main function
            user_prompt = f"""Format this resume:

{extracted_text}

Please format this resume in a professional, clean, and well-structured format."""
            
            try:
                formatted_resume = format_resume_with_agent(user_prompt)
                
                print("\n" + "=" * 80)
                print("Formatted Resume:")
                print("=" * 80)
                print(formatted_resume)
                print("=" * 80)
                
            except Exception as format_error:
                print(f"\nError formatting resume: {format_error}")
                import traceback
                traceback.print_exc()
        else:
            print("\nSkipping resume formatting (format_resume_with_agent not available)")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
