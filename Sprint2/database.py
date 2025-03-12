import sqlite3


def safe_float(value):
    try:
        # If the value is empty or falsy, return 0.0
        return float(value) if value else 0.0
    except ValueError:
        # If it can't be converted, return 0.0
        return 0.0


def create_database_job_postings(db_name='job_postings.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')  # Enable foreign keys

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rapid_results_job_postings (
        id TEXT PRIMARY KEY,
        site TEXT,
        job_url TEXT,
        job_url_direct TEXT,
        title TEXT,
        company TEXT,
        location TEXT,
        job_type TEXT,
        date_posted TEXT,
        salary_source TEXT,
        interval TEXT,
        min_amount REAL,
        max_amount REAL,
        currency TEXT,
        is_remote TEXT,
        emails TEXT,
        description TEXT,
        company_url TEXT,
        company_url_direct TEXT,
        company_addresses TEXT,
        company_num_employees TEXT,
        company_revenue TEXT,
        company_description TEXT,
        logo_photo_url TEXT,
        banner_photo_url TEXT,
        ceo_name TEXT,
        ceo_photo_url TEXT
    )
    ''')

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

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rapid_jobs2_job_providers (
        rapid_jobs2_id TEXT,
        provider_name TEXT,
        provider_url TEXT,
        FOREIGN KEY (rapid_jobs2_id) REFERENCES rapid_jobs2_job_postings(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()


def insert_data_from_job_postings(parsed_data, dbname='job_postings.db'):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()

    for job_list in parsed_data:
        if isinstance(job_list, list):
            for data in job_list:
                if isinstance(data, dict):
                    try:
                        # Insert job posting into rapid_jobs2_job_postings
                        cursor.execute('''
                        INSERT OR REPLACE INTO rapid_jobs2_job_postings (
                            id, title, company, description, location, employmentType, basePayRange, image,
                            datePosted, salaryRange, jobProvider, jobProviderUrl
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            data.get('id', None),
                            data.get('title', ""),
                            data.get('company', ""),
                            data.get('description', ""),
                            data.get('location', ""),
                            data.get('employmentType', ""),
                            data.get('salaryRange', ""),
                            data.get('image', ""),
                            data.get('datePosted', ""),
                            data.get('salaryRange', ""),
                            "",
                            ""
                        ))

                        job_id = data.get('id', None)
                        for provider in data.get('jobProviders', []):
                            provider_name = provider.get('jobProvider', "")
                            provider_url = provider.get('url', "")

                            cursor.execute('''
                            INSERT OR REPLACE INTO rapid_jobs2_job_providers (
                                rapid_jobs2_id, provider_name, provider_url
                            ) VALUES (?, ?, ?)
                            ''', (job_id, provider_name, provider_url))

                    except Exception as e:
                        print(
                            f"Error inserting job posting {data.get('id', 'unknown')}: {e}")

    for data in parsed_data:
        if isinstance(data, dict):  # Ensure it's a dictionary before inserting
            cursor.execute('''
            INSERT OR REPLACE INTO rapid_results_job_postings (
                id, site, job_url, job_url_direct, title, company, location, job_type,
                date_posted, salary_source, interval, min_amount, max_amount, currency,
                is_remote, emails, description, company_url, company_url_direct,
                company_addresses, company_num_employees, company_revenue,
                company_description, logo_photo_url, banner_photo_url, ceo_name, ceo_photo_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('id', ''),
                data.get('site', ''),
                data.get('job_url', ''),
                data.get('job_url_direct', ''),
                data.get('title', ''),
                data.get('company', ''),
                data.get('location', ''),
                data.get('job_type', ''),
                data.get('date_posted', ''),
                data.get('salary_source', ''),
                data.get('interval', ''),
                safe_float(data.get('min_amount', '')),
                safe_float(data.get('max_amount', '')),
                data.get('currency', ''),
                data.get('is_remote', 'False'),
                data.get('emails', ''),
                data.get('description', ''),
                data.get('company_url', ''),
                data.get('company_url_direct', ''),
                data.get('company_addresses', ''),
                data.get('company_num_employees', ''),
                data.get('company_revenue', ''),
                data.get('company_description', ''),
                data.get('logo_photo_url', ''),
                data.get('banner_photo_url', ''),
                data.get('ceo_name', ''),
                data.get('ceo_photo_url', '')
            ))

    conn.commit()
    conn.close()
    print(f"Data successfully inserted into {dbname}")
