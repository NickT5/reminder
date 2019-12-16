from flask import Flask, render_template, request

# Configure app
app = Flask(__name__)

# All tasks
tasks = ["dishes", "fitness"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tasks", methods=["POST"])
def task():
    return render_template("tasks.html", tasks=tasks)

