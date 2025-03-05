import ollama


def generate_resume_ollama(user_job_desc, user_self_desc, model="llama3.2"):
    """
    Generates a resume in Markdown format using an AI model from Ollama.

    Args:
        user_job_desc (str): Job description for the resume.
        user_self_desc (str): Description of the user's skills and experience.
        model (str): The AI model to use (default: "mistral").

    Returns:
        str: Generated resume in Markdown format, or an error message.
    """

    messages = [
        {"role": "system",
         "content": f"You are an AI that helps build a resume in markdown format by analyzing"
                    f" the users description of themselves: "
                    f"\n{user_self_desc}\n "
                    f"and creating a resume for this job: \n{user_job_desc}\n"},
        {"role": "user", "content": f"Generate a resume in markdown format fot this job:\n{user_job_desc}"},
        {"role": "user", "content": f"Here is my background information:\n{user_self_desc}"}
    ]

    try:

        # Generate response from Ollama
        response = ollama.chat(model=model, messages=messages)  # Ensure correct model name

        markdown_content = response.get("message", {}).get("content", "Error: No Generated Content")
        return markdown_content

    except Exception as e:
        return f"Error:{str(e)}"
