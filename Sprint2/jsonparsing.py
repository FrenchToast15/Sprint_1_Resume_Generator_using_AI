import json


def parse_json_file(json_file_name):
    parsed_data = []  # List to store parsed JSON objects

    # Open the JSON file and process each line
    with open(json_file_name, 'r') as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
                try:
                    data = json.loads(line)  # Parse the JSON line
                    parsed_data.append(data)  # Add to list
                except json.JSONDecodeError as e:
                    print(f"Error decoding line: {e}")

    return parsed_data  # Return the list of parsed JSON objects