from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configure app
app = Flask(__name__)
Bootstrap(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Task('{self.id}', '{self.text}')"


# All tasks
all_tasks = []


@app.route("/", methods=["GET", "POST"])
def index():
    # Get all tasks from the database.
    all_tasks = Task.query.all()
    return render_template("index.html", all_tasks=all_tasks)


@app.route("/add_task")
def add_task():
    return render_template("add_task.html")


@app.route("/add_task_to_db", methods=["POST"])
def add_task_to_db():
    task_text = request.form.get('task_text')
    new_task = Task(text=task_text)
    db.session.add(new_task)
    db.session.commit()
    print(new_task)

    return redirect(url_for('index'))


@app.route("/edit_task")
def edit_task():
    # todo
    pass


@app.route("/delete_task")
def delete_task():
    id = request.args.get('id')
    Task.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
