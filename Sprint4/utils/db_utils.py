import sqlite3

from flask import flash


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
