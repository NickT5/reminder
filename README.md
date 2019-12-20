# To do platform
Creating a To do platform webapplication using Flask ( Python for the web), HTML, CSS, Bootstrap, SQL.

## Install instructions
Install the necessary dependies by using *requirements.txt* .
```bash
$pip install -r requirements.txt
```

## Create a database
Run the following commands in the terminal.
```bash
$python
$from app import db
$db.create_all()
```
To delete the database you can call the drop_all() function.
```bash
$python
$from app import db
$db.drop_all()
```

## Run the web application
```bash
$flask run
```
This will start up the server and it will tell where to view the application, e.g. *127.0.0.1:5000*