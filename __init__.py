from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask import Flask
import os




app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


csrf = CSRFProtect(app)
app.secret_key = b'_53oi3uriq9pifpff;apl'

UPLOAD_FOLDER = 'static/uploads/'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///" +os.path.join(basedir, "web.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)
