from database import create_database_job_postings, insert_data_from_job_postings
from jsonparsing import parse_json_file

json_filename = 'rapidResults.json'
parsed_data = parse_json_file(json_filename)  # Parses JSON File

json_filename2 = 'rapid_jobs2.json'
parsed_data2 = parse_json_file(json_filename2)

# Creates database
create_database_job_postings()

# Inserts data from Parsed JSON into database
insert_data_from_job_postings(parsed_data)
insert_data_from_job_postings(parsed_data2)