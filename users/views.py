# IMPORTS
import bcrypt
import pyotp
from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_user
from markupsafe import Markup

from app import db
from models import User
from users.forms import RegisterForm, LoginForm

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
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

        # sends user to login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # 4 COMMENT
    form = LoginForm()

    if not session.get('authentication_attempts'):
        session['authentication_attempts'] = 0

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email_check.data).first()
        if not user \
                or not bcrypt.checkpw(form.password_check.data.encode('utf-8'), user.password): #\
                #or not pyotp.TOTP(user.pin_key).verify(form.pin.data): #Commented code for easier access when testing
            session['authentication_attempts'] += 1
            if session.get('authentication_attempts') == 3:
                flash(Markup('Number of incorrect login attempts exceeded. Please click <a href="/reset">here</a> to '
                             'reset'))
                return render_template('users/login.html')
            attempts_remaining = 3 - session.get('authentication_attempts')
            flash(f'Please check your login details and try again, {attempts_remaining} login attempts remaining')
            return render_template('users/login.html', form=form)
        login_user(user)
        return redirect(url_for('users.profile'))
    return render_template('users/login.html', form=form)


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
def profile():
    return render_template('users/profile.html', name="PLACEHOLDER FOR FIRSTNAME")


# view user account
@users_blueprint.route('/account')
def account():
    return render_template('users/account.html',
                           acc_no="PLACEHOLDER FOR USER ID",
                           email="PLACEHOLDER FOR USER EMAIL",
                           firstname="PLACEHOLDER FOR USER FIRSTNAME",
                           lastname="PLACEHOLDER FOR USER LASTNAME",
                           phone="PLACEHOLDER FOR USER PHONE")
