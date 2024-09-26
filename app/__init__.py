from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)

scheduler = BackgroundScheduler()
scheduler.start()

from app import routes, models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))