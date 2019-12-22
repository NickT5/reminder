from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configure app
app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


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
