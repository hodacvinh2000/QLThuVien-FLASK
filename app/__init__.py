from flask import Flask
import babel
import sqlalchemy
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
 
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

@app.template_filter()
def format_date(value, format):
    return babel.dates.format_datetime(value, format)

from app import routes, models