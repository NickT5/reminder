from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from app.forms import LoginForm
from app.models import User, Task
from datetime import datetime


def custom_datetime(now):
    dt = datetime(now.date().year, now.date().month, now.date().day, now.time().hour, now.time().minute,
                  now.time().second)
    return dt


@login_manager.user_loader
def load_user(user_id):
    """ Because Flask-Login knows nothing about databases, it needs the application's help in loading a user.
    For that reason, the extension expects that the application will configure a user loader function,
     that can be called to load a user given the ID. """
    return User.query.get(int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    # For GET requests, show the login form.
    # For POST requests, check if user may login.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash("Invalid username or password!", "danger")
                return redirect(url_for('login'))
            else:
                login_user(user)
                flash("Login successful.", "success")
                return redirect(url_for('index'))
        else:
            return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Get all tasks from the database.
    todo_tasks = Task.query.filter_by(is_done=False)
    completed_tasks = Task.query.filter_by(is_done=True)
    return render_template("index.html", todo_tasks=todo_tasks, completed_tasks=completed_tasks)


@app.route("/add_form")
@login_required
def add_form():
    return render_template("add_form.html")


@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    task_text = request.form.get('task_text')
    deadline = request.form.get('deadline')
    datetime_created = custom_datetime(datetime.now())
    print(task_text)
    print(deadline)
    print(datetime_created)
    new_task = Task(text=task_text, deadline=deadline, date_created=datetime_created)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/edit_form")
@login_required
def edit_form():
    task_id = request.args.get('id')
    task = Task.query.filter_by(id=task_id).first()
    return render_template("edit_form.html", task=task)


@app.route("/edit_task", methods=["POST"])
@login_required
def edit_task():
    task_id = request.form.get('task_id')
    task_text = request.form.get('task_text')
    deadline = request.form.get('deadline')

    task = Task.query.filter_by(id=task_id).first()
    task.text = task_text
    task.deadline = deadline
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/delete_task")
@login_required
def delete_task():
    task_id = request.args.get('id')
    Task.query.filter_by(id=task_id).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/toggle_state")
@login_required
def toggle_state():
    task_id = request.args.get('id')

    task = Task.query.filter_by(id=task_id).first()
    task.is_done = not task.is_done
    db.session.commit()

    return redirect(url_for('index'))
