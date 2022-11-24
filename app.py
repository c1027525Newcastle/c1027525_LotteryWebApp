# IMPORTS
import logging
import os
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


# Filter class
class SecurityFilter(logging.Filter):
    def filter(self, record):
        """
        Filters through all the log records that enter the function
        :param record: log record
        :return: log records that include the String 'Security'
        """
        return 'Security' in record.getMessage()


# Get the root logger
logger = logging.getLogger()
# Creates a file handler
file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'lottery.log'), 'a')
# Set the level of the file handler
file_handler.setLevel(logging.WARNING)
# Add the filter to the file handler
file_handler.addFilter(SecurityFilter())
# Create a formatter
formatter = logging.Formatter('%(asctime)s : %(message)s', '%m/%d/%Y %I:%M:%S %p')
# Add the formatter to the file handler
file_handler.setFormatter(formatter)
# Add the file_handler to the root logger
logger.addHandler(file_handler)

# CONFIG
# COMMENT on .env
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = os.getenv('SQLALCHEMY_ECHO') == 'True'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'

# COMMENT
app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# initialise database
db = SQLAlchemy(app)


# Wrapper function
def requires_roles(*roles):
    """
    This wrapper function will decorate the functions in lottery/views, admin/views and users/views to control what role
    will have the permission to access different functions
    :param roles: The role or roles that have the permission to access said information or site
    :return: if the role of the user doesn't have permission to the page it will render an error template
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Check if the user that is trying to reach the site is allowed
            if current_user.role not in roles:
                # Add logging statement as log record to the log file
                logging.warning(f'Security - Unauthorised Access Attempt [{current_user.id}, {current_user.email}, '
                                f'{current_user.role}, {request.remote_addr}]')
                return render_template('errors/403.html'), 403
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def anonymous_only(f):
    """
    This wrapper function will decorate login and register functions in users/views to only allow anonymous users to
    access those two function
    :param f: function that is decorated
    :return: if the user is not anonymous it will render an error template
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return render_template('errors/403.html'), 403
        return f(*args, **kwargs)
    return wrapped


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')


# BLUEPRINTS
# import blueprints
from users.views import users_blueprint
from admin.views import admin_blueprint
from lottery.views import lottery_blueprint

# register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(lottery_blueprint)

# COMMENT
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

from models import User


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
###


# Error 400 view
@app.errorhandler(400)
def internal_error(error):
    return render_template('errors/400.html'), 400


# Error 403 view
@app.errorhandler(403)
def internal_error(error):
    return render_template('errors/403.html'), 403


# Error 404 View
@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404


# Error 500 view
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


# Error 503 view
@app.errorhandler(503)
def internal_error(error):
    return render_template('errors/503.html'), 503


if __name__ == "__main__":
    app.run()
