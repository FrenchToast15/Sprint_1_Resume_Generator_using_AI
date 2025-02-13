import sqlite3


def safe_float(value):
    try:
        # If the value is empty or falsy, return 0.0
        return float(value) if value else 0.0
    except ValueError:
        # If it can't be converted, return 0.0
        return 0.0


def create_database_rapid_results(db_name='rapidResults.db'):
    '''
    This function creates a database with a primary key and the following column names
    '''
    conn = sqlite3.connect(
        db_name)  # Use sqlite3.connect() to connect to the database
    cursor = conn.cursor()  # creates a pointer to process DML (Data Manipulation Language)

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
    conn.commit()  # Save the changes
    conn.close()  # Close the connection


def insert_rapid_results_data_into_db(parsed_data, dbname='rapidResults.db'):
    # Use sqlite3.connect() to connect to the database
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()  # creates a pointer to process DML (Data Manipulation Language)

    # loops through each job posting in parsed data (assuming it is a list of
    # dictionaries)
    for data in parsed_data:
        cursor.execute('''
        INSERT OR REPLACE INTO rapid_results_job_postings (
            id, site, job_url, job_url_direct, title, company, location, job_type,
            date_posted, salary_source, interval, min_amount, max_amount, currency,
            is_remote, emails, description, company_url, company_url_direct,
            company_addresses, company_num_employees, company_revenue,
            company_description, logo_photo_url, banner_photo_url, ceo_name, ceo_photo_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            # retrieves the value associated with the key in the dictionary
            # if key is missing, the value will be an empty string
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

    # Commit and close the connection
    conn.commit()  # Saves the changes to the database
    conn.close()  # closes the database
    print(f"Data was successfully inserted into {dbname}")


def create_database_rapid_jobs_2(db_name='rapidjobs2.db'):
    # Use sqlite3.connect() to connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # creates a table in sql if it does not exist
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
        jobProviderUrl TEXT  -- Changed REAL to TEXT for URL storage
    )
    ''')
    conn.commit()  # Save the changes
    conn.close()  # Close the connection


def create_database_rapid_jobs_2_providers(db_name='rapidjobs2.db'):
    # Use sqlite3.connect() to connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Enables the foreign key to work
    cursor.execute('PRAGMA foreign_keys = ON')

    # creates table and creates foreign key
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rapid_jobs2_job_providers (
        rapid_jobs2_id TEXT,
        provider_name TEXT,
        provider_url TEXT,
        FOREIGN KEY (rapid_jobs2_id) REFERENCES rapid_jobs2_job_postings(id)
    )
    ''')
    conn.commit()  # Save the changes
    conn.close()  # Close the connection


def insert_rapid_jobs_2_data_into_db(parsed_data, dbname='rapidjobs2.db'):
    conn = sqlite3.connect(dbname)  # connects to database
    cursor = conn.cursor()

    '''
    In this case, the json is organized a list of list. The file is one big list, with multiple job postings contained inside
    various lists withing the giant list. Ex: [ [{j1},{j2},], [{j3}, {j4}] ]
    '''
    for job_list in parsed_data:  # Iterate through the overall list
        if isinstance(job_list, list):  # Ensure the overall file is a list
            for data in job_list:  # Now iterate through each job posting inside the lists within the giant list
                if isinstance(
                        data, dict):  # Ensure the job posting is a dictionary
                    try:
                        # Insert the job posting into the
                        # rapid_jobs2_job_postings table
                        cursor.execute('''
                        INSERT OR REPLACE INTO rapid_jobs2_job_postings (
                            id, title, company, description, location, employmentType, basePayRange, image,
                            datePosted, salaryRange, jobProvider, jobProviderUrl
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            data.get('id', None),  # id
                            data.get('title', ""),  # title
                            data.get('company', ""),  # company
                            data.get('description', ""),  # description
                            data.get('location', ""),  # location
                            data.get('employmentType', ""),  # employmentType
                            data.get('salaryRange', ""),  # basePayRange
                            data.get('image', ""),  # image
                            data.get('datePosted', ""),  # datePosted
                            data.get('salaryRange', ""),  # salaryRange
                            "",
                            # Placeholder for jobProvider (will be filled
                            # separately)
                            "",
                            # Placeholder for jobProviderUrl (will be filled
                            # separately)
                        ))

                        # After inserting the job posting, insert job providers
                        # associated with it
                        # Store the job posting ID ( we will be using this to
                        # make a foreign key)
                        job_id = data.get('id', None)

                        for provider in data.get(
                            'jobProviders',
                                []):  # gets the jobProviders list from the json parsed data
                            # gets and stores the job provider name and stores
                            # it. if missing it will default to empty strings
                            provider_name = provider.get('jobProvider', "")
                            # same as the line above.
                            provider_url = provider.get('url', "")

                            # Insert each job provider into the
                            # rapid_jobs2_job_providers table
                            cursor.execute('''
                            INSERT OR REPLACE INTO rapid_jobs2_job_providers (
                                rapid_jobs2_id, provider_name, provider_url
                            ) VALUES (?, ?, ?)
                            ''', (job_id, provider_name, provider_url))

                    except Exception as e:  # error handling
                        print(
                            f"Error inserting data for job {data.get('id', 'unknown')}: {e}"
                        )


                else:
                    print(f"Skipping non-dictionary item inside list: {data}")

        else:
            print(f"Skipping non-list item in parsed_data: {job_list}")

    # Saves the database and close the connection
    conn.commit()
    conn.close()
    print(f"Data successfully inserted into {dbname}")
