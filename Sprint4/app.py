from flask import Flask, session

from Sprint4.blueprints.documents import documents_bp
from Sprint4.blueprints.jobs import jobs_bp
from Sprint4.blueprints.personal_info import personal_info_bp
from Sprint4.blueprints.user_profiles import user_profiles_bp
from Sprint4.blueprints.welcome import welcome_info_bp
from utils import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Import blueprints after the app is initialized

# Register blueprints
# All routes will be prefixed with `/`
app.register_blueprint(personal_info_bp, url_prefix="/")
app.register_blueprint(welcome_info_bp, url_prefix="/")  # No prefix
app.register_blueprint(jobs_bp, url_prefix="/jobs")
app.register_blueprint(user_profiles_bp, url_prefix='/profiles')
app.register_blueprint(documents_bp, url_prefix='/documents')


@app.route("/debug_session")
def debug_session():
    return f"<pre>{session}</pre>"


# Run the Flask App
if __name__ == "__main__":
    initialize_user_db()  # Ensure database is created before running
    app.run(debug=True)
