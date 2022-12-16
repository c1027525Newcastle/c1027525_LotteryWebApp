# IMPORTS
import logging
from datetime import datetime

import bcrypt
import pyotp
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required, current_user
from markupsafe import Markup

from app import db, requires_roles, anonymous_only
from models import User
from users.forms import RegisterForm, LoginForm

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
@anonymous_only
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Add logging statement as log record to the log file
        logging.warning(f'Security - User registration [{form.email.data}, {request.remote_addr}]')

        # sends user to login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
@anonymous_only
def login():
    """
    Logs the user in or re-renders the same page with the remaining attempts depending on weather authentication was
    successful
    :return: renders a template
    """
    form = LoginForm()

    # Checks if the authentication_attempts exists and creates it if not
    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email_check.data).first()
        if not user \
                or not bcrypt.checkpw(form.password_check.data.encode('utf-8'), user.password) \
                or not pyotp.TOTP(user.pin_key).verify(form.pin.data):
            session['authentication_attempts'] += 1
            if session.get('authentication_attempts') == 3:
                flash(Markup('Number of incorrect login attempts exceeded. Please click <a href="/reset">here</a> to '
                             'reset'))
                return render_template('users/login.html')

            attempts_remaining = 3 - session.get('authentication_attempts')
            flash(f'Please check your login details and try again, {attempts_remaining} login attempts remaining')

            # Add logging statement as log record to the log file
            logging.warning(f'Security - Invalid Log In Attempt [{form.email_check.data}, {request.remote_addr}]')

            return render_template('users/login.html', form=form)
        # Logs in the user
        login_user(user)

        # Update the last_login with the last login that happened aka current_login
        user.last_login = user.current_login
        # Update current_login with the date and time at the moment the user logs in
        user.current_login = datetime.now()
        db.session.add(user)
        db.session.commit()

        # Add logging statement as log record to the log file
        logging.warning(f'Security - Log in [{user.id}, {user.email}, {request.remote_addr}]')

        # Check the role of the user and redirect him/her to the appropriate link
        if current_user.role == 'user':
            return redirect(url_for('users.profile'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.admin'))
    return render_template('users/login.html', form=form)


# view reset
@users_blueprint.route('/reset')
def reset():
    """
    Resets the authentication_attempts to 0 so the user will be
    able again to try accessing his account
    :return: redirects back to the login page
    """
    session['authentication_attempts'] = 0
    return redirect(url_for('users.login'))


# view user profile
@users_blueprint.route('/profile')
@login_required
@requires_roles('user')
def profile():
    return render_template('users/profile.html', name=current_user.firstname)


# view user account
@users_blueprint.route('/account')
@login_required
@requires_roles('user', 'admin')
def account():
    return render_template('users/account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone)


# view logout
@users_blueprint.route('/logout')
@login_required
def logout():
    """
    Logs out the user thus returning to current_user.is_anonymous
    :return: renders the main/index.html
    """
    # Add logging statement as log record to the log file
    logging.warning(f'Security - Log out [{current_user.id}, {current_user.email}, {request.remote_addr}]')

    logout_user()
    return render_template('main/index.html')
