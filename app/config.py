"""
Setting an environment variable:
- set <envname>=<envvalue> for windows
- export <envname>=<envvalue> for linux
"""
import os


class Config(object):
    """
    The Config class holds configuration variables of the application.
    """
    FLASK_APP = "run.py"
    FLASK_ENV = "development"  # "production"
    DEBUG = True

    # Define the application directory.
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Define secret key.
    SECRET_KEY = os.environ.get("SECRET_KEY") or b'\x955\x7f\x07\xe7\x00\xf7{\x0f\x9a\xafdW\xc7\xdcS'
    
    # Define the database connection.
    if FLASK_ENV == 'development':
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"  # mysql://root:@localhost/todo-platform
    elif FLASK_ENV == 'production':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # From Heroku Postgresql database.
    else:
        print("Environment variable 'FLASK_ENV' not set. Exiting ...")
        exit()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
