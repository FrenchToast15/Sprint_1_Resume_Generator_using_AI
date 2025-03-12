# Utils for resume generation and document conversion
import ollama
from flask import flash, redirect, url_for

from Sprint4.utils.file_and_path_utils import get_output_paths, save_file, convert_md_to_pdf


# ========= RESUME GENERATION =========

def generate_resume_using_ai(user_job_desc, user_self_desc, model="llama3.2"):
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
        response = ollama.chat(model=model, messages=messages)
        markdown_content = response.get("message", {}).get("content", "").strip()

        if not markdown_content:
            return "Error: AI did not return any content."

        return markdown_content
    except Exception as e:
        print(f"Error while generating resume: {str(e)}")  # Debug-friendly output
        return f"Error: {str(e)}"


# ========= MAIN ENTRY POINT =========

def generate_and_convert_resume(user_job_desc, user_self_desc, profile):
    """
    Main function to generate a resume and convert it to a PDF.
    """
    # Generate resume
    resume_markdown = generate_resume_using_ai(user_job_desc, user_self_desc)

    print("\n==== DEBUG: LLM Response ====")
    print(resume_markdown)
    print("=================================\n")

    # Handle AI generation errors
    if resume_markdown.startswith("Error:"):
        flash(resume_markdown, "error")
        return redirect(url_for("jobs.job_postings"))

    # Get output file paths
    paths = get_output_paths(profile)
    markdown_path = paths["markdown"]
    pdf_path = paths["pdf"]

    # Save the Markdown file
    try:
        save_file(resume_markdown, markdown_path)
        flash(f"Resume generated successfully! Filename: {markdown_path}", "success")
    except Exception as e:
        flash(f"Error saving the resume: {str(e)}", "error")
        return redirect(url_for("jobs.job_postings"))

    # Convert Markdown to PDF
    try:
        convert_md_to_pdf(markdown_path, pdf_path)
        flash(f"Resume successfully converted to PDF! Filename: {pdf_path}", "success")
    except Exception as e:
        flash(f"Error converting resume to PDF: {str(e)}", "error")
        return redirect(url_for("jobs.job_postings"))
