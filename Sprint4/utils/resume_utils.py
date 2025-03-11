# Utils for resume generation and document conversion
import os
import re
import markdown
import ollama
from xhtml2pdf import pisa
from flask import flash, redirect, url_for

from Sprint4.app import MD_DIR, PDF_DIR


# You may need to import "ollama" from the corresponding library/package.

def generate_resume_ollama(user_job_desc, user_self_desc, model="llama3.2"):
    """
    Generates a resume in Markdown format using an AI model from Ollama.
    """
    """
    Generates a resume in Markdown format using an AI model from Ollama.
    """
    messages = [
        {"role": "system",
         "content": "You are an AI that generates resumes and cover letters in Markdown format. "
                    "Analyze the user's information and tailor the resume and cover letter to the job description."},
        {"role": "user",
         "content": f"Generate a resume and cover letter in Markdown format for the following job:\n\n"
                    f"### Job Description:\n{user_job_desc}\n\n"
                    f"### User Background:\n{user_self_desc}"}
    ]

    try:
        # Generate response from Ollama
        response = ollama.chat(model=model, messages=messages)

        # Debugging: Print full response
        print("\n==== DEBUG: Full AI Response ====")
        print(response)
        print("=================================\n")

        # Extract Markdown content
        markdown_content = response.get("message", {}).get("content", "").strip()

        if not markdown_content:
            return "Error: AI did not return any content."

        return markdown_content

    except Exception as e:
        print(f"Error: {str(e)}")  # Print error for debugging
        return f"Error: {str(e)}"



def convert_md_to_pdf(md_file, pdf_file):
    """
    Converts a Markdown file to a PDF.
    """
    try:
        # Read the markdown file
        with open(md_file, 'r') as f:
            md_content = f.read()

        # Clean the Markdown content
        cleaned_content = clean_markdown(md_content)

        # Convert markdown to HTML
        html_content = markdown.markdown(cleaned_content)

        # Convert HTML to PDF using xhtml2pdf
        with open(pdf_file, "wb") as pdf:
            pisa.CreatePDF(html_content, dest=pdf)
        print(f"PDF successfully saved to {pdf_file}")
    except Exception as e:
        print(f"Error converting markdown to PDF: {e}")
        raise


def clean_markdown(md_content):
    """
    Removes unwanted Markdown syntax, such as inline code and code blocks.
    """
    # Remove code blocks (triple backticks)
    md_content = re.sub(r'```[\s\S]*?```', '', md_content)

    # Remove inline code (backticks)
    md_content = re.sub(r'`[^`]*`', '', md_content)

    # You can add more regex patterns here to clean other undesired parts of the Markdown.

    return md_content


def generate_and_convert_resume(user_job_desc, user_self_desc, profile):
    """
    Generates the resume in Markdown format and converts it to PDF.
    """

    # Generate resume using Ollama
    resume_markdown = generate_resume_ollama(user_job_desc, user_self_desc)

    print("\n==== DEBUG: LLM Response ====")
    print(resume_markdown)  # Check if it's empty or contains an error
    print("=================================\n")

    if resume_markdown.startswith("Error:"):
        flash(resume_markdown, "error")
        return redirect(url_for("jobs.job_postings"))

    # Save the generated resume as a Markdown file (without converting to PDF yet)
    resume_filename = f"{profile}_resume.md"
    try:
        with open(resume_filename, "w") as f:
            f.write(resume_markdown)
        flash(f"Resume generated successfully! Filename: {resume_filename}", "success")
    except Exception as e:
        flash(f"Error saving the resume: {str(e)}", "error")
        return redirect(url_for("jobs.job_postings"))

    # Convert Markdown to PDF after saving
    try:
        pdf_filename = f"{profile}_resume.pdf"
        convert_md_to_pdf(resume_filename, pdf_filename)
        flash(f"Resume successfully converted to PDF! Filename: {pdf_filename}", "success")
    except Exception as e:
        flash(f"Error converting resume to PDF: {str(e)}", "error")

    return redirect(url_for("documents.view_resume", profile=profile))


def save_files(profile, markdown_content, pdf_content):
    # File paths
    markdown_file_path = os.path.join(MD_DIR, f"{profile}.md")
    pdf_file_path = os.path.join(PDF_DIR, f"{profile}.pdf")

    # Save Markdown content
    with open(markdown_file_path, "w") as md_file:
        md_file.write(markdown_content)

    # Save PDF content
    with open(pdf_file_path, "wb") as pdf_file:
        pdf_file.write(pdf_content)

    print(f"Saved Markdown: {markdown_file_path}")
    print(f"Saved PDF: {pdf_file_path}")

