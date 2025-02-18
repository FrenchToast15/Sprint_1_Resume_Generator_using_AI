from database import (
    create_database_rapid_results,
    insert_rapid_results_data_into_db,
    insert_rapid_jobs_2_data_into_db,
    create_database_rapid_jobs_2,
    create_database_rapid_jobs_2_providers,
)
from jsonparsing import parse_json_file

json_filename = "rapidResults.json"
parsed_data = parse_json_file(json_filename)  # Parses JSON File

create_database_rapid_results()  # creates database
# Inserts parsed data into database
insert_rapid_results_data_into_db(parsed_data)

json_filename2 = "rapid_jobs2.json"
parsed_data2 = parse_json_file(json_filename2)

create_database_rapid_jobs_2()
create_database_rapid_jobs_2_providers()
insert_rapid_jobs_2_data_into_db(parsed_data2)
