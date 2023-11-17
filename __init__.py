from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask import Flask,session,redirect
import os
from functools import wraps



app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


csrf = CSRFProtect(app)
app.secret_key = b'_53oi3uriq9pifpff;apl'

UPLOAD_FOLDER = 'static/uploads/'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///" +os.path.join(basedir, "db/website.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/user_login")
        return f(*args, **kwargs)
    return decorated_function