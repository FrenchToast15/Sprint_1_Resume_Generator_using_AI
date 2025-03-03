import os
import sqlite3
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

def get_users_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize database
def initialize_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create profile table
    cursor.execute('''CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                fname TEXT,
                lname TEXT
            )
        ''')

    # Create user_information table linked to profile
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_information (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER,
    fname TEXT,
    lname TEXT,
    email TEXT,
    phone TEXT,
    location TEXT,
    linkedin TEXT,
    github TEXT,
    portfolio TEXT,
    School TEXT,
    projects TEXT,
    classes TEXT,
    other TEXT,
    FOREIGN KEY (profile_id) REFERENCES profile(id)
            )
        ''')

    conn.commit()
    conn.close()

# Initialize DB when the app starts
initialize_db()

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/profile_creation")
def profile_creation():
    return render_template("profile_creation.html")

@app.route("/submitted_profile", methods=['POST'])
def submit_profile():
    if request.method == 'POST':
        user_data = (
            request.form.get('username'),
            request.form.get('fname'),
            request.form.get('lname')
        )

        print(f"Submitted Data: {user_data}")  # Debugging print

        try:
            profile_id = save_profile_info(user_data)
            print(f"Profile ID: {profile_id}")  # Debugging print
            return redirect(url_for('profiles'))
        except sqlite3.IntegrityError:
            flash("Username already exists! Choose a different username.")
            print("Username already exists")  # Debugging print
            return redirect(url_for('profile_creation'))

    return "Form submission error", 400

# Function to save profile and return its ID
def save_profile_info(user_data):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(''' 
        INSERT INTO profile (username, fname, lname) 
        VALUES (?, ?, ?)''', user_data)

    profile_id = cursor.lastrowid  # Get the inserted profile's ID
    conn.commit()
    conn.close()

    return profile_id  # Return the new profile ID

@app.route("/profiles")
def profiles():
    # Displays profile entries from the database
    conn = get_users_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM profile")
    profiles = cursor.fetchall()

    conn.close()

    profile_count = len(profiles)

    return render_template("select_profile.html", profiles=profiles, profile_count=profile_count)


@app.route("/profile/<int:profile_id>/personal_info", methods=['GET', 'POST'])
def personal_info(profile_id):
    conn = get_users_db_connection()
    cursor = conn.cursor()

    # Fetch the selected profile details
    cursor.execute("SELECT * FROM profile WHERE id = ?", (profile_id,))
    profile = cursor.fetchone()

    if request.method == 'POST':
        # Collect the submitted form data
        user_info = (
            profile_id,  # Link to the profile
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

        # Save the user information to the database
        save_user_information(user_info)

        return redirect(url_for('profile_details', profile_id=profile_id))  # Redirect to profile details page

    # Check if the user information exists already
    cursor.execute("SELECT * FROM user_information WHERE profile_id = ?", (profile_id,))
    user_info = cursor.fetchone()

    conn.close()

    if profile:
        return render_template("personal_info.html", profile=profile, user_info=user_info)
    else:
        return "Profile not found", 404


# Function to save the user information into the database
def save_user_information(user_info):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(''' 
        INSERT INTO user_information (
            profile_id, fname, lname, email, phone, location,
            linkedin, github, portfolio, School, projects, classes, other
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', user_info)

    conn.commit()
    conn.close()

@app.route("/profile_details/<int:profile_id>")
def profile_details(profile_id):
    conn = get_users_db_connection()
    cursor = conn.cursor()

    # Fetch the profile and user information
    cursor.execute("SELECT * FROM profile WHERE id = ?", (profile_id,))
    profile_info = cursor.fetchone()

    cursor.execute("SELECT * FROM user_information WHERE profile_id = ?", (profile_id,))
    user_info = cursor.fetchone()

    conn.close()

    if profile_info:
        if user_info:
            return render_template("profile_details.html", profile_info=profile_info, user_info=user_info)
        else:
            flash("No personal information available. Please fill in the form.", "info")
            return redirect(url_for('personal_info', profile_id=profile_id))
    else:
        return "Profile details not found", 404

if __name__ == "__main__":
    app.run(debug=True)
