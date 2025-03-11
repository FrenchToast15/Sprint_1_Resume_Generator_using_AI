# Prepare user profile session data
from flask import session


def prepare_user_profile_session():
    session['user_profile_info'] = f"""
    Name: {session.get('fname', 'N/A')} {session.get('lname', 'N/A')}
    Email: {session.get('email', 'N/A')}
    Phone: {session.get('phone', 'N/A')}
    Location: {session.get('location', 'N/A')}
    LinkedIn: {session.get('linkedin', 'N/A')}
    GitHub: {session.get('github', 'N/A')}
    Portfolio: {session.get('portfolio', 'N/A')}
    School: {session.get('school', 'N/A')}
    Projects: {session.get('projects', 'N/A')}
    Classes: {session.get('classes', 'N/A')}
    Other Info: {session.get('other_info', 'N/A')}
    """
# Prepare job information session data
def prepare_job_info_session():
    session['job_info'] = f"""
    Job Title: {session.get('job_title', 'N/A')}
    Company: {session.get('job_company', 'N/A')}
    Description: {session.get('job_description', 'N/A')}
    """
