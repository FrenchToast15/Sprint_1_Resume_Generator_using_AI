Sprint4 Overview:

This project delivers a complete application that enables users to manage personalized profiles, select job postings, and programmatically generate customized cover letters and resumes using a language model (LLM). This project uses llama3.2 locally. The final documents (the cover letter and resume and created together and put in one doc) are saved to markdown files, converted to PDFs, and properly structured for the specific job and user information.
Key Features
1.	User Profiles Management
o	Users can create and manage multiple profiles, each containing distinct personal and professional information (e.g., education, projects, classes, etc.).
o	Profiles are stored in an SQLite database and can be retrieved or updated as needed.
o	Once a Profile is created, it cannot be modified
2.	Job Selection
o	The application allows users to select one job and view detailed job information.
o	There is a link that will bring them to the page where the job posting is (if available)
o	There is also a button at the bottom of the page that you can press if you want to generate a resume and cover letter
3.	LLM Integration
o	Generates a customized cover letter in markdown format based on the selected job and user profile.
o	Generates a customized resume in markdown format using the same data.
o	Saves both markdown outputs to files and converts them to PDF format programmatically.
4.	Markdown-to-PDF Conversion
o	Converts the markdown cover letter and resume to high-quality PDFs for submission.
5.	Automated Testing
o	Tests ensure the reliability of the database, LLM interactions, and key application logic, including prompts.
________________________________________
Test Coverage
Here’s how the test functions map to the features and cases in the application:
Test Coverage
1. test_get_db_connection
•	Validates that a connection can be established with the SQLite database.
•	Ensures the database is accessible and functions properly.
2. test_save_file
•	Ensures the save_file function correctly writes content to a specified file path.
•	Mocks file writing to prevent real file system modifications during tests.
3. test_clean_markdown
•	Validates that markdown is properly sanitized by removing unnecessary formatting.
4. test_convert_markdown_to_html
•	Ensures markdown is successfully converted to HTML format.
5. test_convert_md_to_pdf
•	Verifies that Markdown files are correctly converted to PDFs.
•	Uses mocking to test PDF creation without generating real files.
6. test_generate_resume_ollama
•	Confirms that the AI model successfully generates resume content based on user input.
•	Ensures the response is not empty or an error message.
7. test_ollama_response
•	Checks if the AI model API returns a 200 OK response.
•	Ensures connectivity with the local AI server.
8. test_generated_prompt_contains_job_and_user_info
•	Ensures the generated resume includes relevant job description and user profile details.
•	Checks for key information such as job title, programming languages, experience duration, and education.


Each of these tests ensures the critical components of the application function as specified in the Sprint4 deliverable.
________________________________________
How to Set Up and Run the Program
1. Prerequisites
Before running the program or tests, ensure the following are installed and properly configured on your machine:
1.	Python 3.7+
o	The application is written in Python and requires version 3.7 or later.
o	Check if Python is installed with:
python --version
•	If it’s not installed, download it from Python.org.
2.	pip (Python Package Installer)
	Check if pip is installed with:
pip --version
•	Install pip if it’s not present on your system.
3.	Install Required Python Libraries
	Run the following command in the terminal to install all dependencies:
pip install -r requirements.txt
Dependencies include:
•	sqlite3: Built-in with Python for database handling.
•	pytest: Used for running tests.
•	markdown-pdf: For markdown-to-PDF conversion.
•	Additional libraries for connecting to the LLM/API (e.g., openai).
________________________________________
2. Setting Up the Project
Follow these steps to set up the application:
Configuring Ollama
1.	Ensure Ollama is installed and running on your local machine:
2.	Download and install Ollama from Ollama's official website.
3.	Start Ollama's local server (if it doesn't start automatically):
4.	ollama run llama3.2
5.	Confirm Ollama is running by testing the API endpoint:
6.	curl http://localhost:11434/api/generate -d '{"model":"llama3.2", "prompt":"Hello!", "stream":false}'
7.	A successful response means Ollama is correctly configured.
8.	Initialize the database:
o	The database will be automatically created and initialized when the program runs for the first time.
o	Alternatively, you can run the initialize_user_db function in db_utils.py to pre-create the necessary table.
________________________________________
3. Running the Program
You can run the application as follows:
1.	Navigate to the Sprint4 folder in the terminal:
cd Sprint4
2.	Run the program:
python main.py
•	If main.py is not the entry point, use the correct entry script for your implementation.
3.	Follow the prompts to:
o	Select a job.
o	Create and manage user profiles.
o	Generate a cover letter.
o	Generate a resume.
o	Convert markdown files into PDFs.
The final PDFs will be saved to the directory of generated_files in Sprint4 during program execution.
________________________________________
4. Running the Tests
To ensure the application works as expected, run the test suite included in test_db_utils.py:
1.	Run the following command from the Sprint4 directory:
pytest
2.	Expected Output:
o	Successful test cases will display as "passed."
o	Failures will be shown with details about what went wrong.
________________________________________
4.	Database Management
o	Uses SQLite to store user profiles.
o	The user_information table is initialized with fields such as profile_name, fname, lname, email, phone, location, linkedin, github, portfolio, school, projects, classes, and other_info.
o	Database functions include:
	get_db_connection(db_name): Establishes a connection to the database.
	initialize_user_db(): Creates the user_information table if it doesn’t exist.
	save_personal_info(user_data): Saves a new profile to the database while ensuring profile names are unique.
Job_posting.db is included in the Sprint4 folder to help populate jobs in the flask window.
________________________________________
Troubleshooting
If you encounter issues, here are some steps you can take to resolve them:
1.	Ensure all dependencies are installed correctly. If necessary, rerun:
pip install -r requirements.txt
2.	Verify that your Python version is 3.7 or higher:
python --version
3.	If LLM integration fails:
o	Confirm your API key is correctly configured in the .env file.
o	Check your internet connection.
4.	For database-related issues, reinitialize the database by running initialize_user_db().
________________________________________
Conclusion
The Sprint4 application is a robust tool for generating personalized cover letters and resumes programmatically. By following the setup and execution instructions above, you can run the program and its associated tests painlessly on your machine. If you encounter any issues, refer to the troubleshooting section for assistance.
________________________________________
Let me know if further refinement is needed!


=======================================================================

Sprint 3:

Job Posting & Personal Information Web App

This is a Flask-based web application that allows users to submit personal information and view job postings from a database.

Features:
Submit personal information through a form
Save user data into a SQLite database
Display the latest user entry
View job postings from two different sources
Click on job postings to see more details

Technologies Used:
Python (Flask)
SQLite
HTML & Jinja2 Templates

Installation:
Clone the repository:

git clone <repo-url>
cd <repo-folder>

Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install dependencies:
pip install flask

Run the application:
python app.py

Open a browser and go to http://127.0.0.1:5000/.

Database:
The application uses two SQLite databases:

users_personal_information.db for storing personal information

job_postings.db for job postings

Tables are created automatically if they do not exist.



==============================

Sprint 2 Job Data Processing Project

Overview
=================================
This project processes job postings from JSON files and stores them in an SQLite database.
It includes: JSON parsing, Database creation & data insertion, Automated testing using pytest,
Continuous Integration (CI) with GitHub Actions

File Descriptions
🔹 Sprint2/jsonparsing.py

Reads job data from a JSON file line by line.
Converts each line into a Python dictionary.
Returns a list of parsed job objects.

🔹 Sprint2/database.py
Creates and manages the SQLite database.
Contains functions to:
Create tables (job_postings, job_providers).
Insert job data from parsed JSON.
Handle errors gracefully.

🔹 Sprint2/main.py
Main execution file that:
Calls JSON parsing functions.
Creates necessary database tables.
Inserts parsed job data into the database.

🔹 tests/test_jsonparsing.py
Tests parse_json_file() function to ensure:
Correct number of job postings are parsed.
Data is correctly extracted.

🔹 tests/test_database.py
Tests database functions:
Ensures tables are created correctly.
Verifies data insertion and retrieval.

🔹 .github/workflows/test.yml
Defines CI/CD automation:
Runs flake8 for linting.
Executes pytest to validate functionality.
Ensures code quality before merging.

Installation & Setup

1️ Clone the Repository
clone this repository

2️ Create a Virtual Environment (Optional but Recommended)
On macOS/Linux
python3 -m venv venv
source venv/bin/activate

On Windows
python -m venv venv
venv\Scripts\activate

Once activated, your terminal will show (venv), meaning you're working inside the virtual environment.

3️ Install Dependencies
pip install -r requirements.txt
This installs:
SQLite3 (Built into Python)
pytest (For testing)
flake8 (For linting)

Any other dependencies needed for the project.

4️ Set Up the Database
Before inserting data, create the database schema.
python -c "from Sprint2.database import create_database_rapid_jobs_2, create_database_rapid_jobs_2_providers; create_database_rapid_jobs_2(); create_database_rapid_jobs_2_providers()"
This ensures that:
The job postings table is created.
The job providers table is set up.

5️ Run the Application
python Sprint2/main.py

This will:
Parse job postings from JSON files.
Insert them into the database.
Print any errors or missing data.

6️ Running Tests (Optional)
pytest tests/
If all tests pass, you should see output like:

==================== test session starts ====================
collected 2 items

test_jsonparsing.py ✓
test_database.py ✓

==================== 2 passed in 0.25s =====================

7️ Linting (Code Formatting Check)
To check for any coding style issues, use flake8:
flake8 .
If there are errors, fix them before pushing changes.

CI/CD: GitHub Actions Integration
The project includes GitHub Actions for Continuous Integration (CI):
Every push or pull request to master triggers:
Linting (flake8)
Unit Testing (pytest)
The workflow ensures that all commits meet quality standards before merging.

=============================================================================================

Resume Generator using Ollama and JSON Contained In Sprint1 Folder

This program allows users to generate a resume in Markdown format using the Ollama AI model Specifically llama3.2.
The user provides their job description and a personal summary of their skills, and the AI generates a structured resume
in markdown format.

Prerequisites

Before running this script, ensure you have the following installed:

1. Install Python

Ensure you have Python 3.8+ installed.

If not installed, download it from python.org.

2. Install Ollama

Ollama is required to run the AI model locally.

Install Ollama by running:

curl -fsSL https://ollama.com/install.sh | sh

Check if Ollama is installed:

3. Download the Ollama AI Model

The script uses the Llama 3.2 model. Download it using:

ollama pull llama3.2

To verify available models:

ollama list

4. Install Python Dependencies

This script requires the json module (which is built into Python). However, ensure your environment is set up correctly:

pip install --upgrade pip

Usage

Follow these steps to run the script:

Clone this repository or copy the script.

Open a terminal and/or programming environment to run the program/set of codes.

Run the script

Enter your job description and personal set of skills you have when prompted.

The AI-generated resume will be printed and saved as response.json.
The AI-generated resume will be created based off the job description and the personal information and skills
you provided and make a resume that suited for that job.

Output File

The generated resume will be stored in response.json in Markdown format.

To view it properly, open it in a Markdown editor such as VS Code, Obsidian, or GitHub Markdown Preview.