from ToDo_project_files import db, login
from flask_login import UserMixin #handling sessions providing features like "isAuthenticated"

#login manager by flask that returns the current user's id
@login.user_loader
def user(user_id):
    return User.query.get(int(user_id))

#User model for defining columns in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

#(1-many relatonship) since one user can have many tasks
    tasks = db.relationship('Todo', backref='user', lazy=True)

    def __repr__(self):
        return "User details: {} {}".format(self.username, self.email)


#task list display model
class Todo(db.Model):
    __searchable__ = ['tasks']

    id = db.Column(db.Integer, primary_key = True)
    tasks = db.Column(db.Text, nullable = False)
    marked_complete = db.Column(db.Boolean, default = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
#constructor created for the tasks entered by users to be stored
    def __init__(self, tasks):
        self.tasks = tasks
        
    def __repr__(self):
        return "Task Planned: {}".format(self.tasks)


#creating the database
db.create_all()