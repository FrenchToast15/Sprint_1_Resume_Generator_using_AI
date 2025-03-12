# ========= FILE MANAGEMENT =========
import re
from pathlib import Path

import markdown
from xhtml2pdf import pisa


def get_output_paths(profile):
    """
    Gets the paths for saving Markdown and PDF files.
    """
    sprint4_folder = Path(__file__).parent.parent
    markdown_folder = sprint4_folder / "generated_files" / "markdowns"
    pdf_folder = sprint4_folder / "generated_files" / "pdfs"

    # Ensure directories exist
    markdown_folder.mkdir(parents=True, exist_ok=True)
    pdf_folder.mkdir(parents=True, exist_ok=True)

    return {
        "markdown": markdown_folder / f"{profile}_resume.md",
        "pdf": pdf_folder / f"{profile}_resume.pdf"
    }


def save_file(content, filepath):
    """
    Helper function to save text content to a file.
    """
    with open(filepath, "w") as f:
        f.write(content)


# ========= MARKDOWN CLEANING =========

def clean_markdown(md_content):
    """
    Removes unwanted Markdown syntax, such as inline code and code blocks.
    """
    # Remove code blocks (triple backticks)
    md_content = re.sub(r'```[\s\S]*?```', '', md_content)

    # Remove inline code (backticks)
    md_content = re.sub(r'`[^`]*`', '', md_content)

    return md_content


# ========= MARKDOWN TO PDF CONVERSION =========

def convert_markdown_to_html(md_content):
    """
    Converts cleaned Markdown text to HTML.
    """
    return markdown.markdown(md_content)


def save_pdf_from_html(html_content, pdf_file_path):
    """
    Converts HTML content to a PDF file and saves it.
    """
    with open(pdf_file_path, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
        if pisa_status.err:
            raise Exception("Failed to generate PDF")


def convert_md_to_pdf(md_file, pdf_file):
    """
    Reads Markdown file, cleans it, and converts the content to a PDF.
    """
    try:
        # Read and clean Markdown file
        with open(md_file, 'r') as f:
            md_content = f.read()

        cleaned_content = clean_markdown(md_content)

        # Convert to HTML, then PDF
        html_content = convert_markdown_to_html(cleaned_content)
        save_pdf_from_html(html_content, pdf_file)

        print(f"PDF successfully saved to {pdf_file}")
    except Exception as e:
        print(f"Error during Markdown to PDF conversion: {e}")
        raise
