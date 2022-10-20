# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# CONFIG
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialise database
db = SQLAlchemy(app)


# HOME PAGE VIEW
@app.route('/')
def index():
    return render_template('main/index.html')


# BLUEPRINTS
# import blueprints
from users.views import users_blueprint
from admin.views import admin_blueprint
from lottery.views import lottery_blueprint
#
# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(lottery_blueprint)


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
