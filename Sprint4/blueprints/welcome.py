from flask import Blueprint, render_template

# Initialize the blueprint
welcome_info_bp = Blueprint(
    "welcome_info", __name__, template_folder="../templates")


# Home Page
@welcome_info_bp.route("/")
def welcome():
    # Ensure 'welcome.html' exists in '/templates'
    return render_template("welcome.html")
