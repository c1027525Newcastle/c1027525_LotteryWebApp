from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from users.validation import excludes_character_check, contains_check, phone_format_check


# COMMENT and check what was already written here at the start as to comment only the new code
class RegisterForm(FlaskForm):
    # DO I NEED TO COMMENT THIS?
    email = StringField(validators=[DataRequired(), Email()])
    firstname = StringField(validators=[DataRequired(), excludes_character_check])
    lastname = StringField(validators=[DataRequired(), excludes_character_check])
    phone = StringField(validators=[DataRequired(), phone_format_check])
    password = PasswordField(validators=[DataRequired(), Length(min=6, max=12), contains_check])
    # CAN I ADD EXTRA? e.g. Length to confirm_password
    confirm_password = PasswordField(validators=[DataRequired(), Length(min=6, max=12),
                                                 EqualTo('password', message='Both passwords must be equal!')])
    submit = SubmitField()


# 4 COMMENT
class LoginForm(FlaskForm):
    email_check = StringField(validators=[DataRequired()])
    password_check = PasswordField(validators=[DataRequired()])
    pin = StringField(validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField()
