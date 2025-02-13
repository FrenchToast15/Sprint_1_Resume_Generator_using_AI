import json


def parse_json_file(json_file_name):
    parsed_data = []  # List to store each parsed JSON objects

    # Open the JSON file and process each line in reading mode
    # with open function automatically opens and closes the
    with open(json_file_name, 'r') as f:
        for line in f: #iterates over the file line by line
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # If line is empty, skip empty lines
                try:
                    data = json.loads(line)  # Parse the JSON line (converts JSON string into Python Dictionary)
                    parsed_data.append(data)  # Adds the parsed data to the list
                except json.JSONDecodeError as e: #if JSON format incorrect, error is caught
                    print(f"Error decoding line: {e}")

    return parsed_data  # Return the list of parsed JSON objects