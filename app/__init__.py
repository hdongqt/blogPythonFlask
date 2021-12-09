from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e891e54508a90a3ff07cb8d33a3f1fee'
app.config.from_object(Config)
app.run(debug=True)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

migrate = Migrate(app, db) 
login = LoginManager(app)
login.login_view = 'login'
login.login_message_category = 'info'

from app import  routes, models