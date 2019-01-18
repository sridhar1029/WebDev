from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#configs
app = Flask(__name__)
app.config['SECRET_KEY'] = '2d18235222308352904cf7104a580a6c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #three slaches means relative path from current file
db = SQLAlchemy(app)

from flaskblog import routes