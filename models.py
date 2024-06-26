from datetime import datetime

import bcrypt
import pyotp
from cryptography.fernet import Fernet
from flask_login import UserMixin

from app import db, app


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='user')

    # Encryption key for the lottery draw
    lottery_draw_key = db.Column(db.BLOB, nullable=True)

    # Pin key for the time based pin authentication
    pin_key = db.Column(db.String(100), nullable=False)

    # Records the date and time the user created his account
    registered_on = db.Column(db.DateTime, nullable=False)

    # Records the date and time of the current login session
    current_login = db.Column(db.DateTime, nullable=True)

    # Records the date and time of the last login
    last_login = db.Column(db.DateTime, nullable=True)

    # Define the relationship to Draw
    draws = db.relationship('Draw')

    def __init__(self, email, firstname, lastname, phone, password, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        # Encrypt password
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        self.role = role
        # Generate the encryption key for the draws of each user
        self.lottery_draw_key = Fernet.generate_key()

        # Generate the pin key
        self.pin_key = pyotp.random_base32()

        self.registered_on = datetime.now()
        self.current_login = None
        self.last_login = None


class Draw(db.Model):
    __tablename__ = 'draws'

    id = db.Column(db.Integer, primary_key=True)

    # ID of user who submitted draw
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    # 6 draw numbers submitted
    numbers = db.Column(db.String(100), nullable=False)

    # Draw has already been played (can only play draw once)
    been_played = db.Column(db.BOOLEAN, nullable=False, default=False)

    # Draw matches with master draw created by admin (True = draw is a winner)
    matches_master = db.Column(db.BOOLEAN, nullable=False, default=False)

    # True = draw is master draw created by admin. User draws are matched to master draw
    master_draw = db.Column(db.BOOLEAN, nullable=False)

    # Lottery round that draw is used
    lottery_round = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, user_id, numbers, master_draw, lottery_round, draw_key):
        self.user_id = user_id
        self.numbers = encrypt(numbers, draw_key)
        self.been_played = False
        self.matches_master = False
        self.master_draw = master_draw
        self.lottery_round = lottery_round

    def view_lottery_draw(self, draw_key):
        """
        Calls another function to decrypt the draw
        :param draw_key: Key of the corresponding user to the draw
        :return: Nothing
        """
        self.numbers = decrypt(self.numbers, draw_key)


def encrypt(data, draw_key):
    """
    Encrypt the draw that comes in with the draw_key given
    :param data: The exact draw chosen
    :param draw_key: Encryption key
    :return: Draw encrypted
    """
    return Fernet(draw_key).encrypt(bytes(data, 'utf-8'))


def decrypt(data, draw_key):
    """
    Decrypts the draw that comes in with the draw_key given
    :param data: The ciphertext that needs to be decrypted
    :param draw_key: Encryption key with which the data was encrypted
    :return: Draw decrypted
    """
    return Fernet(draw_key).decrypt(data).decode('utf-8')


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@email.com',
                     password='Admin1!',
                     firstname='Alice',
                     lastname='Jones',
                     phone='0191-123-4567',
                     role='admin')

        db.session.add(admin)
        db.session.commit()
