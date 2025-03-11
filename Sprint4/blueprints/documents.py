import werkzeug
from werkzeug.utils import secure_filename
from flask import Blueprint, session, redirect, url_for, flash, render_template, send_from_directory
from Sprint4.constants import MD_DIR, PDF_DIR  # Import from constants
from Sprint4.utils import generate_and_convert_resume, save_files  # Assuming this is a helper function

documents_bp = Blueprint('documents', __name__)



@documents_bp.route("/generate_docs/<profile>/<job>", methods=['POST'])
def generate_doc(profile, job):
    # Debug Session Data
    print("\n==== DEBUG: Session Data Before LLM Request ====")
    print(session)
    print("===============================================\n")

    # Extract profile and job data from the session
    user_job_desc = session.get('job_info')
    user_self_desc = session.get('user_profile_info')

    if not user_job_desc or not user_self_desc:
        flash("Missing profile or job data. Please select again.", "error")
        return redirect(url_for('select_profile'))

    # Generate Markdown and PDF content
    markdown_content = f"# Resume for {profile}\n\nJob Description:\n{user_job_desc}\n\nProfile Info:\n{user_self_desc}"
    pdf_response = generate_and_convert_resume(user_job_desc, user_self_desc, profile)  # corrected call

    # Check the type of pdf_response and handle appropriately
    if isinstance(pdf_response, str):
        # Handle string response (e.g., error messages)
        if pdf_response.startswith("Error:"):
            flash(pdf_response, "error")
            return redirect(url_for('select_profile'))
    elif isinstance(pdf_response, bytes):
        # Handle valid PDF binary content
        pdf_content = pdf_response
    else:
        # Handle unexpected response types
        flash("Unexpected error: Invalid response from PDF generation.", "error")
        return redirect(url_for('user_profiles.select_profile'))

    # Save files to the appropriate folders
    save_files(profile, markdown_content, pdf_content)

    return f"Files for {profile} saved successfully!"


@documents_bp.route("/view_resume/<profile>")
def view_resume(profile):
    # Construct the URL for the PDF file from the 'pdfs' folder
    pdf_url = url_for("documents.serve_pdf", filename=f"{profile}.pdf")  # Use the custom route
    return render_template("resume_display.html", profile=profile, pdf_url=pdf_url)


# Route to serve Markdown files
@documents_bp.route("/markdown/<filename>")
def serve_markdown(filename):
    safe_filename = werkzeug.utils.secure_filename(filename)  # Make filename safe
    return send_from_directory(MD_DIR, safe_filename)


# Route to serve PDF files
@documents_bp.route("/pdf/<filename>")
def serve_pdf(filename):
    safe_filename = werkzeug.utils.secure_filename(filename)  # Make filename safe
    return send_from_directory(PDF_DIR, safe_filename)


