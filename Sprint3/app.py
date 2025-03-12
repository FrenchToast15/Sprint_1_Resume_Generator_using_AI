import sqlite3

from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


# Function to get a database connection
def get_db_connection(db_name='job_postings.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row  # Allow dictionary-style access
    return conn


@app.route("/")
def welcome():
    # returns the welcome.html
    return render_template("welcome.html")


@app.route("/personal_info", methods=['GET'])
def personal_info():
    return render_template("personal_info.html")


@app.route("/submitted_info", methods=['POST'])
def submit_info():
    # saves the information submitted from the personal_info.html
    if request.method == 'POST':
        user_data = (
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

        save_personal_info(user_data)

        return redirect(url_for('display_info'))

    return "Form submission error", 400


# Function to save form data to the database
def save_personal_info(user_data):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user_information (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fname TEXT, lname TEXT, email TEXT, phone TEXT, location TEXT,
        linkedin TEXT, github TEXT, portfolio TEXT,
        school TEXT, projects TEXT, classes TEXT, other_info TEXT
    )''')

    cursor.execute('''INSERT INTO user_information (fname, lname, email, phone, location,
     linkedin, github, portfolio, school, projects, classes, other_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', user_data)

    conn.commit()
    conn.close()


@app.route("/display_info")
# Displays latest entry to user
def display_info():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_information ORDER BY id DESC LIMIT 1")
    user_data = cursor.fetchone()
    conn.close()

    return render_template("submitted_info.html", user_data=user_data)


@app.route("/job_postings")
def job_postings():
    # Displays job posting entries from database
    conn = get_db_connection('job_postings.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, title, company, location FROM rapid_results_job_postings")
    jobs1 = cursor.fetchall()

    cursor.execute(
        "SELECT id, title, company, location FROM rapid_jobs2_job_postings")
    jobs2 = cursor.fetchall()

    conn.close()

    all_jobs = jobs1 + jobs2
    job_count = len(all_jobs)

    return render_template("job_postings.html", jobs=all_jobs, job_count=job_count)


@app.route("/job/<job_id>")
# Displays more details of job posting when clicked on
def job_details(job_id):
    conn = get_db_connection('job_postings.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM rapid_results_job_postings WHERE id = ?", (job_id,))
    job = cursor.fetchone()

    if not job:
        cursor.execute(
            "SELECT * FROM rapid_jobs2_job_postings WHERE id = ?", (job_id,))
        job = cursor.fetchone()

    conn.close()

    # If job found, render job details page, else return 404
    if job:
        return render_template("job_details.html", job=job)
    else:
        return "Job not found", 404  # Using a simple string message


if __name__ == "__main__":
    app.run(debug=True)
