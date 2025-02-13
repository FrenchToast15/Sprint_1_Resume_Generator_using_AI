import sqlite3
import json
import os
from Sprint2.database import insert_rapid_jobs_2_data_into_db

def create_tables(dbname='test_rapidjobs2.db'):
    '''
    setting up the tables so we can test the database in the other function.
    '''
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    # Create job postings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rapid_jobs2_job_postings (
        id TEXT PRIMARY KEY,
        title TEXT,
        company TEXT,
        description TEXT,
        location TEXT,
        employmentType TEXT,
        basePayRange TEXT,
        image TEXT,
        datePosted TEXT,
        salaryRange TEXT,
        jobProvider TEXT,
        jobProviderUrl TEXT
    )
    ''')

    # Create job providers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rapid_jobs2_job_providers (
        rapid_jobs2_id TEXT,
        provider_name TEXT,
        provider_url TEXT,
        FOREIGN KEY (rapid_jobs2_id) REFERENCES rapid_jobs2_job_postings(id)
    )
    ''')

    conn.commit()
    conn.close()


def test_insert_and_retrieve():
    '''
    Testing the creation and insertion of data into a database.
    '''

    test_db = 'test_rapidjobs2.db'

    # Ensure the test database is new
    if os.path.exists(test_db):
        os.remove(test_db)

    #Create tables
    create_tables(test_db)

    #Insert a test job
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

    # Insert test data
    insert_rapid_jobs_2_data_into_db(test_data, test_db)

    # Verify the data
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    # Query job postings table
    cursor.execute("SELECT * FROM rapid_jobs2_job_postings WHERE id = ?", ("test_123",))
    job_result = cursor.fetchone()

    # Query job providers table
    cursor.execute("SELECT * FROM rapid_jobs2_job_providers WHERE rapid_jobs2_id = ?", ("test_123",))
    provider_results = cursor.fetchall()

    conn.close()

    # Testing to see if we can get desired results
    assert job_result is not None, "Test job was not inserted!"
    assert len(provider_results) == 2, "Test job providers were not inserted correctly!"

    print("Test passed: Data inserted and verified successfully!")


# Runs the test
test_insert_and_retrieve()
