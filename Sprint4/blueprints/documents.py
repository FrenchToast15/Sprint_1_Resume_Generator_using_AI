from flask import Blueprint, session, redirect, url_for, flash

from Sprint4.utils import generate_and_convert_resume  # Assuming this is a helper function

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
        return redirect(url_for('user_profiles.select_profile'))

    # Generate PDF content
    pdf_response = generate_and_convert_resume(user_job_desc, user_self_desc, profile)

    # Handle errors during PDF generation
    if isinstance(pdf_response, str) and pdf_response.startswith("Error:"):
        flash(pdf_response, "error")
        return redirect(url_for('user_profiles.select_profile'))

    # If the response is valid but unexpected, handle the edge case
    if not isinstance(pdf_response, bytes):
        flash("Unexpected error: Invalid response from PDF generation.", "error")
        return redirect(url_for('user_profiles.select_profile'))

    # Success case
    flash(f"Files for {profile} saved successfully!", "success")
    return f"Files for {profile} saved successfully!"
