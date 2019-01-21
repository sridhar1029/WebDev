from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

#configs
app = Flask(__name__)
app.config['SECRET_KEY'] = '2d18235222308352904cf7104a580a6c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #three slaches means relative path from current file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sdng123@gmail.com'
app.config['MAIL_PASSWORD'] = 'Zebraa1029'
mail = Mail(app)

from flaskblog import routes