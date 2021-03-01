from flask import render_template, redirect, request, flash
from ToDo_project_files import app, db, bcrypt
from ToDo_project_files.models import User, Todo
from ToDo_project_files.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user


#displays the homepage
@app.route("/")
def home_page():
    return render_template("home.html")


#registeration processing route
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/task/" + str(current_user.id))
    form = RegistrationForm()
    if form.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=password_hashed)
        db.session.add(user)
        db.session.commit()
        flash("Account Created! Please login.")
        return redirect("/login")
    return render_template("register.html", title='Register', form=form)


#login processing route
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/task/" + str(current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect("/task/" + str(current_user.id))
        else:
            flash('Login Failed!')
    return render_template("login.html", title='Login', form=form)


#route that will display all tasks of that specific logged in user
@app.route("/task/<int:get_id>")
def display_tasks(get_id):
    if current_user.is_authenticated:
        tasking = User.query.get(get_id)
        task_list = tasking.tasks
        return render_template("display.html", task_list = task_list)
    else:
        return redirect("/register")


#for adding new tasks and redirecting back to homescreen to display
@app.route("/task/<int:get_id>/add-task", methods = ["GET", "POST"])
def add_task(get_id):
    task = request.form["fetch_task"]
    if task:
        new_task = Todo(task) #creating an instance for the model
        new_task.user = current_user #fetching details of the current logged in users who create a task
        if get_id == current_user.id:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/task/" + str(get_id))
    else:
        raise Exception("Please check the input!")


#for updating a particular task
@app.route("/task/<int:get_userid>/edit-task/<int:get_id>", methods = ["GET", "POST"])
def edit_task(get_userid, get_id):
    task = request.form["edit_task"]
    if task:
        fetch = Todo.query.filter_by(id = get_id).first()
        if get_userid == current_user.id:
            fetch.tasks = task
            db.session.commit()
            return redirect('/task/' + str(get_userid))
    else:
        raise Exception("Please enter the updated task!")

        
#for deleting a particular task
@app.route("/task/<int:get_userid>/delete-task/<int:get_id>")
def delete_task(get_userid, get_id):
    fetched_task = Todo.query.get(get_id)
    if get_userid == current_user.id:
        db.session.delete(fetched_task)
        db.session.commit()
        return redirect("/task/" + str(get_userid))
    else:
        raise Exception("Attempt Failed! Please try again!")

        
#striking of or unstriking (Mark as done) a task
@app.route("/task/<int:get_userid>/completed/<int:get_id>")
def mark_as_complete(get_userid, get_id):
    fetched_task = Todo.query.get(get_id)
    if get_userid == current_user.id:
        if fetched_task.marked_complete:
            fetched_task.marked_complete = False
        else:
            fetched_task.marked_complete = True
        db.session.commit()
        return redirect("/task/" + str(get_userid))
    else:
        raise Exception("Attempt Failed! Please try again!")


#searching for tasks based on __searchable__ in model
@app.route("/task/<int:get_id>/search")
def search(get_id):
    tasks = Todo.query.whoosh_search(request.args.get('query')).all()
    if get_id == current_user.id:
        return render_template("/task/" + str(get_id), task_list=tasks)
    else:
        raise Exception("Attempt Failed!")


#logging out process for current user
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

