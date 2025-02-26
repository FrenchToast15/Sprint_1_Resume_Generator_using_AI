import sqlite3

import pytest

from Sprint3.app import app, get_db_connection


def test_get_db_connection():
    # Get a connection to an in-memory database
    conn = get_db_connection(':memory:')

    # Ensure the connection is valid
    assert isinstance(conn, sqlite3.Connection)

    # Ensure the row factory is set to sqlite3.Row
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
    """Creates a test client for the Flask app."""
    app.testing = True
    with app.test_client() as client:
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

    # Assert the response status is 200 OK
    assert response.status_code == 200

    # Check if the response contains the expected content (a heading personal_info.html)
    assert b"Personal Information" in response.data  # Assuming there's a heading with this text

    # Checks for input element in `personal_info.html`)
    assert b'<input' in response.data  # Check if there is an <input> tag in the page
