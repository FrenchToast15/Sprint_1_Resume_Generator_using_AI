import ollama

user_job_desc_ = input("Please insert your job description: ")
print(user_job_desc_)

user_describe_yourself =  input("Please insert your a description of you and your skills: ")
print(user_describe_yourself)

messages=[
    {"role": "system", "content": "You are a AI that helps builds a resume in markdown format." },
    {"role": "user", "content": user_job_desc_},
    {"role": "user", "content":  user_describe_yourself}
]
response = ollama.chat(model="llama3.2", messages=messages)


print(response["message"]["content"])