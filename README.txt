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