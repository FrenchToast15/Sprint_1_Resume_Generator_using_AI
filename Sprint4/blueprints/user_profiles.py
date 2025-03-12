from flask import Blueprint, render_template, session, redirect, url_for, request

from Sprint3.app import save_personal_info
from Sprint4.utils import get_db_connection, prepare_user_profile_session

user_profiles_bp = Blueprint('user_profiles', __name__)


# Select Profile Page
@user_profiles_bp.route("/select_profile", methods=['GET', 'POST'])
def select_profile():
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, profile_name FROM user_information")
    profiles = cursor.fetchall()
    conn.close()

    if request.method == 'POST':
        selected_profile_id = request.form.get('profile_id')

        # Fetch full profile details from the database
        conn = get_db_connection("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user_information WHERE id = ?", (selected_profile_id,))
        profile = cursor.fetchone()
        conn.close()

        if profile:
            # Store full profile details in session
            session['selected_profile_id'] = selected_profile_id
            session['profile_name'] = profile['profile_name']
            session['fname'] = profile['fname']
            session['lname'] = profile['lname']
            session['email'] = profile['email']
            session['phone'] = profile['phone']
            session['location'] = profile['location']
            session['linkedin'] = profile['linkedin']
            session['github'] = profile['github']
            session['portfolio'] = profile['portfolio']
            session['school'] = profile['school']
            session['projects'] = profile['projects']
            session['classes'] = profile['classes']
            session['other_info'] = profile['other_info']

            # Prepare formatted session data
            prepare_user_profile_session()
            print("Session Data:", session)

        # Redirect after selection
        return redirect(url_for('jobs.job_postings'))

    return render_template("select_profile.html", profiles=profiles, profile_count=len(profiles))


# Profile Details Page
@user_profiles_bp.route("/profile/<int:profile_id>")
def profile_details(profile_id):
    # Fetch profile details using the utility function
    profile = save_personal_info(profile_id)

    if profile:
        # Save profile details into the session
        session['selected_profile_id'] = profile['id']
        session['profile_name'] = profile['profile_name']
        session['fname'] = profile['fname']
        session['lname'] = profile['lname']
        session['email'] = profile['email']
        session['phone'] = profile['phone']
        session['location'] = profile['location']
        session['linkedin'] = profile['linkedin']
        session['github'] = profile['github']
        session['portfolio'] = profile['portfolio']
        session['school'] = profile['school']
        session['projects'] = profile['projects']
        session['classes'] = profile['classes']
        session['other_info'] = profile['other_info']

        # Optional: Debugging
        print("Session Data Updated:", session)

        # Render the profile details template
        return render_template("profile_details.html", profile=profile)
    else:
        # Return a 404 error if the profile is not found
        return "Profile not found", 404
