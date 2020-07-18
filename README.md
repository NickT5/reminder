# To Do Platform
This project is a To Do web application build with Flask, SQL, HTML, CSS and Bootstrap. Flask is a (micro) Python web framework. 
The application is deployed on Heroku which is a platform to build, run, and operate applications entirely in the cloud.

Note: it takes a while to spin up the application. Click [here](https://todo-platform.herokuapp.com/) to check it out.

## How to run the app locally 

### 1. Install the dependencies
Install the necessary dependencies by using *requirements.txt* .
```bash
pip install -r requirements.txt
```

### 2. Create a database
Run the following commands in the terminal.
```bash
python
from app import db
db.create_all()
```
To delete the database you can call the drop_all() function.
```bash
python
from app import db
db.drop_all()
```

### 3. Run the web application
```bash
python run.py
```
This will start up the server and it will tell where to view the application, e.g. *127.0.0.1:5000*