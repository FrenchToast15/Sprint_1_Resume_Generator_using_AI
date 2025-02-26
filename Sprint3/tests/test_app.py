import sqlite3
import uuid
from unittest.mock import patch

import pytest
from flask import url_for

from Sprint3.app import app, get_db_connection  # save_personal_info


def test_get_db_connection():
    # Get a connection to an in-memory database
    conn = get_db_connection(':memory:')

    # Ensure the connection is valid
    assert isinstance(conn, sqlite3.Connection)

    # Ensures row factory is set to sqlite3.Row
    assert conn.row_factory == sqlite3.Row

    # Create a test table
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO test (name) VALUES (?)", ("Alice",))
    conn.commit()

    # Query the test table
    cursor.execute("SELECT * FROM test WHERE name = ?", ("Alice",))
    row = cursor.fetchone()

    # Ensure the row exists and can be accessed like a dictionary
    assert row is not None
    assert row["name"] == "Alice"

    # Close the connection
    conn.close()


@pytest.fixture()
def client():
    # Set up the test client
    with app.test_client() as client:
        # Use SQLite's in-memory database for testing
        conn = sqlite3.connect(':memory:')  # Create an in-memory database
        conn.row_factory = sqlite3.Row  # Access rows by column name

        # Create necessary tables for testing in the in-memory database
        conn.execute('CREATE TABLE personal_info (id INTEGER PRIMARY KEY, fname TEXT, lname TEXT, email TEXT)')
        conn.commit()
        conn.close()

        # Set the Flask app to use the in-memory database by updating the app's config
        app.config['DATABASE'] = ':memory:'  # Update your app to point to the in-memory database

        # Run the test
        yield client


def test_welcome_route(client):
    """Tests if the welcome page loads correctly."""

    response = client.get("/")
    assert response.status_code == 200  # Check if the response is OK
    # Check if the response contains the expected heading text
    assert b"Pick Available Jobs or Enter information about yourself" in response.data  # Check for the <h1> text

    # Check for the button text or the button's appearance
    assert b'Job Postings' in response.data  # Check if the button "Job Postings" is there
    assert b'Enter Personal Info' in response.data  # Check if the button "Enter Personal Info" is there


def test_personal_info_route(client):
    """Test if the personal info page loads correctly."""
    response = client.get("/personal_info")

    # Checks to see if response status is 200
    assert response.status_code == 200

    # Check if the response contains the following
    assert b"Personal Information" in response.data  # Assuming there's a heading with this text

    # Checks for input element in `personal_info.html`
    assert b'<input' in response.data


def test_job_details(client):
    """Test if the /job/<job_id> route displays the correct job details."""

    job_id = str(uuid.uuid4())  # Generates a random UUID as a job_id

    # Mock the database connection and query response
    conn = sqlite3.connect('job_postings.db')
    cursor = conn.cursor()

    # Insert a test job into the database
    cursor.execute('''INSERT INTO rapid_results_job_postings (id, title, company, location)
                      VALUES (?, ?, ?, ?)''', (job_id, 'Software Engineer', 'Tech Corp', 'San Francisco'))
    conn.commit()
    conn.close()

    # Send GET request to /job/<job_id>
    response = client.get(f"/job/{job_id}")  # Use the generated job_id in the URL

    # Check to see the response status is 200
    assert response.status_code == 200

    # Check if the job title is in the response
    assert b"Software Engineer" in response.data
    assert b"Tech Corp" in response.data
    assert b"San Francisco" in response.data

    # Check if job details page loads in correctly
    assert b"Job Details" in response.data  # Making sure includes this title


def test_job_details_404(client):
    """Test if the /job/<job_id> route returns a 404 when the job is not found."""

    nonexistent_job_id = "f97b4a007d08a432"  # Example of a non-existent job ID

    # Send GET request to /job/<nonexistent_job_id>
    response = client.get(f"/job/{nonexistent_job_id}")

    # Check the response status is 404 Not Found
    assert response.status_code == 404

    # Check if the job not found message is in the response
    assert b"Job not found" in response.data


def test_submit_info(client, mocker):
    """Test if the /submitted_info route correctly processes the form and redirects."""

    # test the form data
    form_data = {
        'fname': 'John',
        'lname': 'Doe',
        'email': 'johndoe@example.com',
        'phone': '1234567890',
        'location': 'San Francisco',
        'linkedin': 'https://linkedin.com/in/johndoe',
        'github': 'https://github.com/johndoe',
        'portfolio': 'https://johndoe.com',
        'School': 'University of Example',
        'projects': 'Project 1, Project 2',
        'classes': 'Class A, Class B',
        'other': 'Additional info'
    }

    # Use mocker.patch to mock save_personal_info function
    mock_save = mocker.patch('Sprint3.app.save_personal_info')

    # Test a POST request with the form data
    response = client.post('/submitted_info', data=form_data)

    # CHeck that save_personal_info was called with the correctly
    mock_save.assert_called_once_with(tuple(form_data.values()))

    # Check that the response is a redirect to the display_info route
    assert response.status_code == 302  # Redirect status code
    assert response.location == url_for('display_info')


# def test_save_personal_info():
#     """Test if the save_personal_info function correctly inserts data into the database."""
# 
#     # Sample form data
#     form_data = (
#         'John', 'Doe', 'johndoe@example.com', '1234567890', 'San Francisco',
#         'https://linkedin.com/in/johndoe', 'https://github.com/johndoe', 'https://johndoe.com',
#         'University of Example', 'Project 1, Project 2', 'Class A, Class B', 'Additional info'
#     )
# 
#     # Correct patch to your app's specific path where sqlite3 is used
#     with patch('Sprint3.app.sqlite3.connect') as mock_connect:  # Use the correct path here
#         mock_cursor = mock_connect.return_value.cursor.return_value
# 
#         # Call the save_personal_info function
#         save_personal_info(form_data)
# 
#         # Check if the cursor's execute method was called with the expected SQL query
#         mock_cursor.execute.assert_any_call('''INSERT INTO users (fname, lname, email, phone, location,
#             linkedin, github, portfolio, school, projects, classes, other_info)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', form_data)
# 
#         # Check if commit and close were called
#         mock_connect.return_value.commit.assert_called_once()
#         mock_connect.return_value.close.assert_called_once()


def test_display_info(client):
    """Test if the /display_info route retrieves and displays the correct user data."""

    # Mock the database connection and cursor

    with patch('sqlite3.connect') as mock_connect:
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = {
            'id': 1, 'fname': 'John', 'lname': 'Doe', 'email': 'johndoe@example.com',
            'phone': '1234567890', 'location': 'San Francisco', 'linkedin': 'https://linkedin.com/in/johndoe',
            'github': 'https://github.com/johndoe', 'portfolio': 'https://johndoe.com',
            'school': 'University of Example',
            'projects': 'Project 1, Project 2', 'classes': 'Class A, Class B', 'other_info': 'Additional info'
        }

        # Test the GET request to /display_info
        response = client.get('/display_info')

        # Check if the response status code 200 or good
        assert response.status_code == 200

        # Check if the correct user data is displayed in the response
        assert b'John' in response.data
        assert b'Doe' in response.data
        assert b'johndoe@example.com' in response.data
        assert b'San Francisco' in response.data

        # Make sure the query gets the lasted data entry
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users ORDER BY id DESC LIMIT 1")
