import requests

from Sprint4.utils import generate_resume_using_ai


def test_generate_resume_ollama():
    user_job_desc = "Software Engineer role at Google"
    user_self_desc = "Experienced Python developer with AI expertise"

    generated_text = generate_resume_using_ai(user_job_desc, user_self_desc)

    assert generated_text, "⚠️ Ollama did not return any response"
    assert not generated_text.startswith(
        "Error"), f"⚠️ Ollama returned an error: {generated_text}"

    print("✅ Ollama is working correctly and generated a resume!")
    print(generated_text)


def test_ollama_response():
    # Ollama's default local API endpoint
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3.2",  # Change this to the model you're using
        "prompt": "Hello!",
        "stream": False
    }

    try:
        response = requests.post(url, json=data)

        assert response.status_code == 200, f"⚠️ Unexpected status code: {response.status_code}"
        print("✅ Ollama returned a 200 OK!")
        print("Response:", response.json())  # Print response for debugging

    except requests.ConnectionError:
        print("❌ Failed to connect to Ollama. Make sure it's running.")


def test_generated_prompt_contains_job_and_user_info():
    # Sample inputs
    job_desc = "Looking for a software engineer with Python and SQL experience."
    user_info = "I have a degree in Computer Science and 3 years of experience with Python."

    # Generate the prompt
    generated_prompt = generate_resume_using_ai(job_desc, user_info)

    # Check if key job description elements exist in the generated output
    assert "software engineer" in generated_prompt.lower(
    ), "❌ Job title missing from generated prompt!"
    assert "python" in generated_prompt.lower(
    ), "❌ Python skill missing from generated prompt!"
    assert "sql" in generated_prompt.lower(), "❌ SQL skill missing from generated prompt!"

    # Check if key user information elements exist in the generated output
    assert "computer science" in generated_prompt.lower(
    ), "❌ Degree information missing from generated prompt!"
    assert "3 years" in generated_prompt.lower(
    ), "❌ Experience duration missing from generated prompt!"

    print("✅ Test passed: The generated resume contains relevant job description and user information.")


if __name__ == "__main__":
    test_ollama_response()
    test_generated_prompt_contains_job_and_user_info()
    test_generate_resume_ollama()
