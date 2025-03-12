import json
import os
import sqlite3

from Sprint2.database import create_database_job_postings, insert_data_from_job_postings
from Sprint2.jsonparsing import parse_json_file


def test_parse_json_file():
    """
    Test if JSON parsing correctly reads job postings from a test file.
    """
    test_json_filename = "test_jobs.json"
    test_data = [
        {"id": "1", "title": "Software Engineer", "company": "TestCorp"},
        {"id": "2", "title": "Data Scientist", "company": "Data Inc."}
    ]

    with open(test_json_filename, "w") as f:
        for item in test_data:
            f.write(json.dumps(item) + "\n")

    parsed_data = parse_json_file(test_json_filename)

    assert len(parsed_data) == 2, "Incorrect number of items parsed!"
    assert parsed_data[0]["title"] == "Software Engineer", "First item title does not match!"
    assert parsed_data[1]["company"] == "Data Inc.", "Second item company does not match!"

    print("✅ Test passed: JSON parsing works correctly!")


def create_test_database(db_name="test_job_postings.db"):
    """
    Creates a test database with required tables.
    """
    create_database_job_postings(db_name)


def test_database_schema():
    """
    Test that the database tables are created with the correct structure.
    """
    test_db = "test_job_postings.db"

    if os.path.exists(test_db):
        os.remove(test_db)

    create_test_database(test_db)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0] for row in cursor.fetchall()}

    assert "rapid_results_job_postings" in tables, "Table rapid_results_job_postings is missing!"
    assert "rapid_jobs2_job_postings" in tables, "Table rapid_jobs2_job_postings is missing!"
    assert "rapid_jobs2_job_providers" in tables, "Table rapid_jobs2_job_providers is missing!"

    # Check column structures
    def get_columns(table_name):
        cursor.execute(f"PRAGMA table_info({table_name});")
        return {row[1] for row in cursor.fetchall()}

    rapid_results_columns = get_columns("rapid_results_job_postings")
    rapid_jobs2_columns = get_columns("rapid_jobs2_job_postings")
    providers_columns = get_columns("rapid_jobs2_job_providers")

    expected_rapid_results_columns = {
        "id", "site", "job_url", "job_url_direct", "title", "company",
        "location", "job_type", "date_posted", "salary_source", "interval",
        "min_amount", "max_amount", "currency", "is_remote", "emails",
        "description", "company_url", "company_url_direct", "company_addresses",
        "company_num_employees", "company_revenue", "company_description",
        "logo_photo_url", "banner_photo_url", "ceo_name", "ceo_photo_url"
    }

    expected_rapid_jobs2_columns = {
        "id", "title", "company", "description", "location",
        "employmentType", "basePayRange", "image", "datePosted",
        "salaryRange", "jobProvider", "jobProviderUrl"
    }

    expected_providers_columns = {
        "rapid_jobs2_id", "provider_name", "provider_url"}

    assert rapid_results_columns == expected_rapid_results_columns, "rapid_results_job_postings schema mismatch!"
    assert rapid_jobs2_columns == expected_rapid_jobs2_columns, "rapid_jobs2_job_postings schema mismatch!"
    assert providers_columns == expected_providers_columns, "rapid_jobs2_job_providers schema mismatch!"

    conn.close()
    print("✅ Test passed: Database schema is correct!")


def test_database_insert_and_retrieve():
    """
    Test inserting and retrieving job data in the merged database.
    """
    test_db = "test_job_postings.db"

    if os.path.exists(test_db):
        os.remove(test_db)

    create_test_database(test_db)

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
                    {"jobProvider": "TestLinkedIn",
                     "url": "https://linkedin.com/test_123"},
                    {"jobProvider": "TestIndeed",
                     "url": "https://indeed.com/test_123"}
                ]
            }
        ],
        {
            "id": "result_001",
            "site": "JobBoard",
            "job_url": "https://example.com/job123",
            "title": "Data Engineer",
            "company": "DataCorp",
            "location": "Remote",
            "job_type": "Full-time",
            "date_posted": "2025-02-10",
            "min_amount": 90000,
            "max_amount": 120000,
            "currency": "USD",
            "is_remote": "True"
        }
    ]

    insert_data_from_job_postings(test_data, test_db)

    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Verify job postings exist
    cursor.execute(
        "SELECT * FROM rapid_jobs2_job_postings WHERE id = ?", ("test_123",))
    job_result = cursor.fetchone()

    cursor.execute(
        "SELECT * FROM rapid_results_job_postings WHERE id = ?", ("result_001",))
    result_job = cursor.fetchone()

    # Verify job providers exist
    cursor.execute(
        "SELECT * FROM rapid_jobs2_job_providers WHERE rapid_jobs2_id = ?", ("test_123",))
    provider_results = cursor.fetchall()

    conn.close()

    assert job_result is not None, "Test job was not inserted into rapid_jobs2_job_postings!"
    assert result_job is not None, "Test job was not inserted into rapid_results_job_postings!"
    assert len(
        provider_results) == 2, "Test job providers were not inserted correctly!"

    print("✅ Test passed: Database insert and retrieve works!")


# Run tests
test_parse_json_file()
test_database_schema()
test_database_insert_and_retrieve()
