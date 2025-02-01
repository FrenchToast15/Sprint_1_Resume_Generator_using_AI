import ollama

response = ollama.chat(model="llama3.2",
                       messages=[{"role": "user", "content": "Posted Job Description you found: "
                                                             "Describe yourself: "
                                                             "llama3.2, give me a sample resume in markdown format that will be designed for my skills and the job description I provided."}])

print(response["message"]["content"])
