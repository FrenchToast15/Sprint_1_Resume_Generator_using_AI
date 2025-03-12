from flask import Blueprint, render_template, session

from Sprint4.utils import get_db_connection
from Sprint4.utils import prepare_job_info_session

jobs_bp = Blueprint('jobs', __name__)


# Display Job Postings
@jobs_bp.route("/job_postings")
def job_postings():
    conn = get_db_connection("job_postings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, company, location FROM rapid_results_job_postings")
    jobs1 = cursor.fetchall()

    cursor.execute("SELECT id, title, company, location FROM rapid_jobs2_job_postings")
    jobs2 = cursor.fetchall()

    conn.close()

    # 🔹 Get selected profile from session
    profile_id = session.get('selected_profile_id')
    profile = None

    if profile_id:
        conn = get_db_connection("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_information WHERE id = ?", (profile_id,))
        profile = cursor.fetchone()
        conn.close()

    all_jobs = jobs1 + jobs2
    return render_template("job_postings.html", jobs=all_jobs, job_count=len(all_jobs), profile=profile)


# Job Details Page
@jobs_bp.route("/job/<job_id>", methods=['GET', 'POST'])
def job_details(job_id):
    conn = get_db_connection("job_postings.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rapid_results_job_postings WHERE id = ?", (job_id,))
    job = cursor.fetchone()

    if not job:
        cursor.execute("SELECT * FROM rapid_jobs2_job_postings WHERE id = ?", (job_id,))
        job = cursor.fetchone()

    conn.close()

    if job:
        # Store job details in session
        session['selected_job_id'] = job_id
        session['job_title'] = job['title']
        session['job_company'] = job['company']
        session['job_location'] = job['location']
        session['job_description'] = job['description']

        # Prepare formatted job session data
        prepare_job_info_session()

        # Debugging: Print job session data to console
        print("Updated Job Session Data:", session)

        return render_template("job_details.html", job=job)
    else:
        return "Job not found", 404
