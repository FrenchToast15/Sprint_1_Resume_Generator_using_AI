import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages




# Function to get a database connection
def get_db_connection(db_name):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Allow dictionary-style access
    return conn


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

def prepare_session_data():
    user_profile_info =f""" 
    Name: {session['fname']} {session['lname']}
    Email: {session['email']}
    Phone: {session['phone']}
    Location: {session['location']}
    LinkedIn: {session['linkedin']}
    GitHub: {session['github']}
    Portfolio: {session['portfolio']}
    School: {session['school']}
    Projects: {session['projects']}
    Classes: {session['classes']}
    Other Info: {session['other_info']}
    """
    job_info = f"""
    {session['job_title']} 
    {session['job_company']} 
    {session['job_description']} 
    """
    return None


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

    if request.method == 'POST':
        selected_job_id = request.form.get('job_id')
        session['selected_job_id'] = selected_job_id  # Store job selection
        return redirect(url_for('generate_docs'))

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
        session['selected_profile_id'] = selected_profile_id  # Store in session
        return redirect(url_for('job_postings'))  # Redirect to job selection

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

@app.route("generate_docs")
def generate_doc():
    return None

# Run the Flask App
if __name__ == "__main__":
    initialize_user_db()  # Ensure database is created before running
    app.run(debug=True)
