import json
import os
import sqlite3

from Sprint2 import jsonparsing, database
from Sprint2.database import insert_rapid_jobs_2_data_into_db, create_database_rapid_jobs_2, \
    create_database_rapid_jobs_2_providers


def test_parse_json_file():
    # Create a temporary JSON file for testing
    test_json_filename = "test_jobs.json"
    test_data = [
        {"id": "1", "title": "Software Engineer", "company": "TestCorp"},
        {"id": "2", "title": "Data Scientist", "company": "Data Inc."}
    ]

    with open(test_json_filename, "w") as f:
        for item in test_data:
            f.write(json.dumps(item) + "\n")

    # Parse the JSON file
    parsed_data = jsonparsing.parse_json_file(test_json_filename)

    # Assertions
    assert len(parsed_data) == 2, "Incorrect number of items parsed!"
    assert parsed_data[0]["title"] == "Software Engineer", "First item title does not match!"
    assert parsed_data[1]["company"] == "Data Inc.", "Second item company does not match!"

    print("Test passed: JSON parsing works correctly!")

# Run test
test_parse_json_file()



def create_test_database(db_name="test_rapidjobs2.db"):
    """
    Creates a test database with required tables.
    """
    create_database_rapid_jobs_2(db_name)  # Creates the main job postings table
    create_database_rapid_jobs_2_providers(db_name)  # Ensures provider table exists

def test_database_insert_and_retrieve():
    """
    Test inserting and retrieving job data.
    """
    test_db = "test_rapidjobs2.db"

    # Ensure a fresh test database
    if os.path.exists(test_db):
        os.remove(test_db)

    create_test_database(test_db)  # Create all required tables

    # Insert test job data
    test_data = [
        [
            {
                "id": "test_123",
                "title": "Software Engineer",
                "company": "Test Corp",
                "description": "Develop test applications...",
                "location": "Test City",
                "employmentType": "Full-time",
                "salaryRange": "$100,000 - $120,000",
                "image": "https://example.com/test.jpg",
                "datePosted": "2025-02-12",
                "jobProviders": [
                    {"jobProvider": "TestLinkedIn", "url": "https://linkedin.com/test_123"},
                    {"jobProvider": "TestIndeed", "url": "https://indeed.com/test_123"}
                ]
            }
        ]
    ]

    insert_rapid_jobs_2_data_into_db(test_data, test_db)

    # Check database contents
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Verify job posting exists
    cursor.execute("SELECT * FROM rapid_jobs2_job_postings WHERE id = ?", ("test_123",))
    job_result = cursor.fetchone()

    # Verify job providers exist
    cursor.execute("SELECT * FROM rapid_jobs2_job_providers WHERE rapid_jobs2_id = ?", ("test_123",))
    provider_results = cursor.fetchall()

    conn.close()

    # Assertions
    assert job_result is not None, "Test job was not inserted!"
    assert len(provider_results) == 2, "Test job providers were not inserted correctly!"

    print("Test passed: Database insert and retrieve works!")

# Run test
test_database_insert_and_retrieve()