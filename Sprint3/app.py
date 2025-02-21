from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Job data
conn = sqlite3.connect('job_postings.db')
cursor = conn.cursor()

# Fetch data from first table
cursor.execute("SELECT * FROM rapid_results_job_postings")
rapid_results_job_postings = cursor.fetchall()

# Fetch data from second table
cursor.execute("SELECT * FROM rapid_jobs2_job_postings")
rapid_jobs2_job_postings = cursor.fetchall()

# Fetch data from third table
cursor.execute("SELECT * FROM rapid_jobs2_job_providers")
rapid_jobs2_job_providers = cursor.fetchall()

conn.close()  # Close the database connection

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/personal_info")
def personal_info():
    return render_template("personal_info.html")

@app.route("/job_postings")
def job_postings():
    # Connect to the SQLite database
    conn = sqlite3.connect("job_postings.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    cursor = conn.cursor()

    # Fetch all job postings
    cursor.execute("SELECT * FROM rapid_results_job_postings")
    jobs = cursor.fetchall()

    conn.close()  # Close the connection

    # Pass jobs to the template
    return render_template("job_postings.html", jobs=jobs)

@app.route("/job/<job_id>")
def job_details(job_id):
    conn = sqlite3.connect("job_postings.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM rapid_results_job_postings WHERE id = ?", (job_id,))
    job = cursor.fetchone()  # Fetch the job from the database

    conn.close()

    return render_template("job_details.html", job=job) if job else ("Job Not Found", 404)


if __name__ == "__main__":
    app.run(debug=True)
