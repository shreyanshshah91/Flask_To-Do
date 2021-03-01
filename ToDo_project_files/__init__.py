from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#import flask_whooshalchemy as wa
#from ToDo_project.models import Todo

app = Flask(__name__)
#used "import secrets, secrets.token_urlsafe(16)" to generate an ehx string for secret key
app.config['SECRET_KEY'] = "xLTtWeCjUgyWR2zw4xXDdQ"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['WHOOSH_BASE'] = "whoosh"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#handles session (login, logout)
login = LoginManager(app)

#linking whoosh alchemy to the ToDo model
#wa.whoosh_index(app, Todo)

from ToDo_project_files import routes