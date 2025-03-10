import re
import sqlite3
from xhtml2pdf import pisa
import markdown
import ollama
from flask import Flask, render_template, request, url_for, redirect, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages




# Function to get a database connection
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Allow dictionary-style access
    return conn


def prepare_session_data():
    session['user_profile_info'] = f""" 
    Name: {session.get('fname', 'N/A')} {session.get('lname', 'N/A')}
    Email: {session.get('email', 'N/A')}
    Phone: {session.get('phone', 'N/A')}
    Location: {session.get('location', 'N/A')}
    LinkedIn: {session.get('linkedin', 'N/A')}
    GitHub: {session.get('github', 'N/A')}
    Portfolio: {session.get('portfolio', 'N/A')}
    School: {session.get('school', 'N/A')}
    Projects: {session.get('projects', 'N/A')}
    Classes: {session.get('classes', 'N/A')}
    Other Info: {session.get('other_info', 'N/A')}
    """

    session['job_info'] = f"""
    Job Title: {session.get('job_title', 'N/A')} 
    Company: {session.get('job_company', 'N/A')} 
    Description: {session.get('job_description', 'N/A')}
    """


# Initialize user database with table
def initialize_user_db():
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_information (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        profile_name TEXT UNIQUE,
        fname TEXT, lname TEXT, email TEXT, phone TEXT, location TEXT,
        linkedin TEXT, github TEXT, portfolio TEXT,
        school TEXT, projects TEXT, classes TEXT, other_info TEXT
    )''')
    conn.commit()
    conn.close()



# Home Page
@app.route("/")
def welcome():
    return render_template("welcome.html")


# Personal Info Form
@app.route("/personal_info", methods=['GET'])
def personal_info():
    return render_template("personal_info.html")


# Handle Form Submission
@app.route("/submitted_info", methods=['POST'])
def submit_info():
    if request.method == 'POST':
        user_data = (
            request.form.get('profile_name'),
            request.form.get('fname'),
            request.form.get('lname'),
            request.form.get('email'),
            request.form.get('phone'),
            request.form.get('location'),
            request.form.get('linkedin'),
            request.form.get('github'),
            request.form.get('portfolio'),
            request.form.get('School'),
            request.form.get('projects'),
            request.form.get('classes'),
            request.form.get('other')
        )

        if save_personal_info(user_data):
            return redirect(url_for('display_info'))
        else:
            return redirect(url_for('personal_info'))  # Stay on form if error

    return "Form submission error", 400


# Save Personal Info to Database (Handles Duplicate Profiles)
def save_personal_info(user_data):
    conn = get_db_connection("users.db")
    cursor = conn.cursor()

    profile_name = user_data[0]

    try:
        cursor.execute('''INSERT INTO user_information (profile_name, fname, lname, email, phone, location, linkedin, github, portfolio, school, projects, classes, other_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', user_data)
        conn.commit()
    except sqlite3.IntegrityError:
        flash(f"Profile name '{profile_name}' already exists! Choose a different name.", "error")
        return False
    finally:
        conn.close()

    return True


# Display Latest Submitted Info
@app.route("/display_info")
def display_info():
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_information ORDER BY id DESC LIMIT 1")
    user_data = cursor.fetchone()
    conn.close()

    return render_template("submitted_info.html", user_data=user_data)


# Display Job Postings
@app.route("/job_postings")
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
@app.route("/job/<job_id>", methods=['GET', 'POST'])
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
        prepare_session_data()

        # Debugging: Print job session data to console
        print("Updated Job Session Data:", session)

        return render_template("job_details.html", job=job)
    else:
        return "Job not found", 404



# Select Profile Page
@app.route("/select_profile", methods=['GET', 'POST'])
def select_profile():
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, profile_name FROM user_information")
    profiles = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        selected_profile_id = request.form.get('profile_id')

        # Fetch full profile details from the database
        conn = get_db_connection("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_information WHERE id = ?", (selected_profile_id,))
        profile = cursor.fetchone()
        conn.close()

        if profile:
            # Store full profile details in session
            session['selected_profile_id'] = selected_profile_id
            session['profile_name'] = profile['profile_name']
            session['fname'] = profile['fname']
            session['lname'] = profile['lname']
            session['email'] = profile['email']
            session['phone'] = profile['phone']
            session['location'] = profile['location']
            session['linkedin'] = profile['linkedin']
            session['github'] = profile['github']
            session['portfolio'] = profile['portfolio']
            session['school'] = profile['school']
            session['projects'] = profile['projects']
            session['classes'] = profile['classes']
            session['other_info'] = profile['other_info']

            # Prepare formatted session data
            prepare_session_data()
            print("Session Data:", session)

        return redirect(url_for('job_postings'))  # Redirect after selection

    return render_template("select_profile.html", profiles=profiles, profile_count=len(profiles))


# Profile Details Page
@app.route("/profile/<int:profile_id>")
def profile_details(profile_id):
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_information WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()
    conn.close()

    if profile:
        return render_template("profile_details.html", profile=profile)
    else:
        return "Profile not found", 404

@app.route("/generate_docs/<profile>/<job>", methods=['POST'])
def generate_doc(profile, job):
    print("\n==== DEBUG: Session Data Before LLM Request ====")
    print(session)
    print("===============================================\n")

    # Extract profile and job data from the session
    user_job_desc = session.get('job_info')  # Assuming job info is already in the session
    user_self_desc = session.get('user_profile_info')  # Assuming profile info is already in the session

    if not user_job_desc or not user_self_desc:
        flash("Missing profile or job data. Please select again.", "error")
        return redirect(url_for('select_profile'))

    # Generate and convert the resume
    return generate_and_convert_resume(user_job_desc, user_self_desc, profile)


def generate_resume_ollama(user_job_desc, user_self_desc, model="llama3.2"):
    """
    Generates a resume in Markdown format using an AI model from Ollama.
    """
    messages = [
        {"role": "system",
         "content": "You are an AI that generates resumes and cover letters in Markdown format. "
                    "Analyze the user's information and tailor the resume and cover letter to the job description."},
        {"role": "user",
         "content": f"Generate a resume in Markdown format for the following job:\n\n"
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
        return redirect(url_for("job_postings"))

    # Save the generated resume as a Markdown file (without converting to PDF yet)
    resume_filename = f"{profile}_resume.md"
    try:
        with open(resume_filename, "w") as f:
            f.write(resume_markdown)
        flash(f"Resume generated successfully! Filename: {resume_filename}", "success")
    except Exception as e:
        flash(f"Error saving the resume: {str(e)}", "error")
        return redirect(url_for("job_postings"))

    # Convert Markdown to PDF after saving
    try:
        pdf_filename = f"{profile}_resume.pdf"
        convert_md_to_pdf(resume_filename, pdf_filename)
        flash(f"Resume successfully converted to PDF! Filename: {pdf_filename}", "success")
    except Exception as e:
        flash(f"Error converting resume to PDF: {str(e)}", "error")

    return redirect(url_for("job_postings"))

@app.route("/debug_session")
def debug_session():
    return f"<pre>{session}</pre>"

# Run the Flask App
if __name__ == "__main__":
    initialize_user_db()  # Ensure database is created before running
    app.run(debug=True)

