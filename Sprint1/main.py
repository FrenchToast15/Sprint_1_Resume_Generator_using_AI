import user_input
from resume_generator import generate_resume_ollama
from save_response import save_to_json

# Get user inputs
user_job = user_input.get_user_job_desc_input()
user_self_desc = user_input.get_user_self_desc_input()

# Generate resume
resume_markdown = generate_resume_ollama(user_job, user_self_desc)

# Print the response in Markdown format
print("\nGenerated Resume (Markdown Format):\n")
print(resume_markdown)

# Save response to JSON
save_to_json(resume_markdown)





