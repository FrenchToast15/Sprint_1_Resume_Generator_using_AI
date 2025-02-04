Resume Generator using Ollama and JSON

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