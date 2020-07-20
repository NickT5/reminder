# RMNDR
RMNDR is an application to remind me what tasks I have to do. The user (me) can add, edit, delete and change the status of 
the tasks which are stored in a database. A python script sends the user an email every day with all the uncompleted tasks.
Authentication is also implemented. The web application is build with Flask, SQL, HTML, CSS, Bootstrap and runs on a Raspberry Pi.
 
Note: The first version of this project was a To Do application run on Heroku which is a platform to build, run and 
operate apps entirely in the cloud. The old version is still up (it takes a couple of seconds to spin up the application).
 Click [here](https://todo-platform.herokuapp.com/) to check it out.

## How to run the app locally 

### 1. Install the dependencies
Install the necessary dependencies by using *requirements.txt* .
```bash
pip install -r requirements.txt
```

### 2. Create a database
Run the following commands in the terminal.
```bash
python3
from app import db
db.create_all()
exit()
```
To delete the database you can call the drop_all() function.
```bash
python3
from app import db
db.drop_all()
exit()
```

### 3. Add a user
Call the add_user.py script and follow the instructions to add a user.
```bash
python3 add_user.py 
````

### 4. Mail functionality
For the mail functionality a gmail account is required. Save the gmail address and password as environment variables in .profile file:
```bash
nano ~/.profile
export EMAIL_USER=<email address>
export EMAIL_PASSWORD=<password>
```
Add a crontab to execute the notify.py script whenever you like. I chose 09:00 every day. [Helpful tool: crontab](https://crontab.guru).
```bash
0 9 * * * . $HOME/.profile; ~/Documents/todo_platform/venv/bin/python3 ~/Documents/todo_platform/notify.py
```

### 5. Run the web application
```bash
python3 run.py
```

### 6. Enter the web application
The application runs on <machine's ip>:5000 e.g. *127.0.0.1:5000*.
The index page will show an unauthorized message. Go to /login.
```
127.0.0.1:5000/login
```