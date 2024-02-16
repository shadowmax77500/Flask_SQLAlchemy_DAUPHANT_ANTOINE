from flask import Flask
from flask_migrate import Migrate
from .database import db
from .models import *

migrate = Migrate()

def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = 'QZDQZDQZDZQZ'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pass@db/hotel'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  from .api import api
  app.register_blueprint(api)

  migrate.init_app(app, db)

  return app