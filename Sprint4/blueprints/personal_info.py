from flask import Blueprint, render_template, request, redirect, url_for

from Sprint4.utils import get_db_connection
# Assuming you have a save_personal_info function
from Sprint4.utils import save_personal_info

# Initialize the blueprint
personal_info_bp = Blueprint(
    "personal_info", __name__, template_folder="../templates")


# Personal Info Form
@personal_info_bp.route("/personal_info", methods=['GET'])
def personal_info():
    return render_template("personal_info.html")


# Handle Form Submission
@personal_info_bp.route("/submitted_info", methods=['POST'])
def submit_info():
    if request.method == 'POST':
        user_data = (
            request.form.get('profile_name'),
            request.form.get('fname'),
            request.form.get('lname'),
            request.form.get('email'),
            request.form.get('phone'),
            request.form.get('location'),
            request.form.get('linkedin'),
            request.form.get('github'),
            request.form.get('portfolio'),
            request.form.get('School'),
            request.form.get('projects'),
            request.form.get('classes'),
            request.form.get('other')
        )

        if save_personal_info(user_data):
            return redirect(url_for('personal_info.display_info'))
        else:
            # Stay on form if error
            return redirect(url_for('personal_info.personal_info'))

    return "Form submission error", 400


# Display Latest Submitted Info
@personal_info_bp.route("/display_info")
def display_info():
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_information ORDER BY id DESC LIMIT 1")
    user_data = cursor.fetchone()
    conn.close()

    return render_template("submitted_info.html", user_data=user_data)
