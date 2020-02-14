from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ

# Configure app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'    # Sqlite database.
# For a sqlite database, you need to have a database.db file in your project root directory.

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/todo-platform'
# driver://user:password@host/database-name
if environ.get('LOCAL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    """
    To use environ.get('SQLALCHEMY_DATABASE_URI'), you have to first set the env variable. On Windows, use set.
    "set KEY=value". See settings.cfg file.
    For a MySQL database, we first need to install a package (pip install mysqlclient). 
    Next, we need to create a database. I used xampp phpMyAdmin to do this. 
    Next, we need to create the database table. We have two options where the latter is the easiest:
    - Create the table using phpMyAdmin with it's columns. This has to match the code. Note: don't forget A_I checkbox
     for auto increment the id column.
    - Open up a terminal and run:
      > python
      > from app import db
      > db.create_all()
      > db.session.commit()
    """
else:
    pass  # Add postgresql here.

Bootstrap(app)
db = SQLAlchemy(app)


def custom_datetime(now):
    dt = datetime(now.date().year, now.date().month, now.date().day, now.time().hour, now.time().minute, now.time().second)
    return dt


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.text}')"


@app.route("/", methods=["GET", "POST"])
def index():
    # Get all tasks from the database.
    todo_tasks = Task.query.filter_by(is_done=False)
    completed_tasks = Task.query.filter_by(is_done=True)
    return render_template("index.html", todo_tasks=todo_tasks, completed_tasks=completed_tasks)


@app.route("/add_form")
def add_form():
    return render_template("add_form.html")


@app.route("/add_task", methods=["POST"])
def add_task():
    task_text = request.form.get('task_text')
    datetime_created = custom_datetime(datetime.now())
    new_task = Task(text=task_text, date_created=datetime_created)
    db.session.add(new_task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/edit_form")
def edit_form():
    task_id = request.args.get('id')
    task = Task.query.filter_by(id=task_id).first()
    return render_template("edit_form.html", task=task)


@app.route("/edit_task", methods=["POST"])
def edit_task():
    task_id = request.form.get('task_id')
    task_text = request.form.get('task_text')

    task = Task.query.filter_by(id=task_id).first()
    task.text = task_text
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/delete_task")
def delete_task():
    task_id = request.args.get('id')
    Task.query.filter_by(id=task_id).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/toggle_state")
def toggle_state():
    task_id = request.args.get('id')

    task = Task.query.filter_by(id=task_id).first()
    task.is_done = not task.is_done
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
