import ollama
import json

# Get user inputs
user_job_desc_ = input("Please insert your job description: ")
print(user_job_desc_)

user_describe_yourself = input("Please insert a description of you and your skills: ")
print(user_describe_yourself)

# Set up messages for Ollama
messages = [
    {"role": "system", "content": "You are an AI that helps build a resume in markdown format by analyzing the user_describe_yourself and making it fit the user_job_desc_"},
    {"role": "user", "content": user_job_desc_},
    {"role": "user", "content": user_describe_yourself}
]

# Generate response from Ollama
response = ollama.chat(model="llama3.2", messages=messages)  # Ensure correct model name

# Extract Markdown content from the response
markdown_content = response["message"]["content"]

print("\nResponse from Ollama:")
print(markdown_content)

# Save only the Markdown text to JSON
data = {"markdown": markdown_content}

with open("response.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)  # Ensure readable formatting

print("\nResponse saved to response.json")
