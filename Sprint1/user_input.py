def get_user_job_desc_input():
    """Gets user input for job description and personal description."""
    user_job_desc = input("Enter the job description: ")
    print("\nJob Description:\n", user_job_desc)

    return user_job_desc


def get_user_self_desc_input():
    user_self_desc = input("\nEnter a description of yourself and your skills."
                           "Make Sure to include the following: Name, College/University attended or graduated from,"
                           "Related coursework, Technical skills(programing languages and frameworks,"
                           "Relevant Projects and Achievements,"
                           "Previous Job Experiences, and Personal qualities:   "
                           " ")
    print("\nYour Description:\n", user_self_desc)

    return user_self_desc