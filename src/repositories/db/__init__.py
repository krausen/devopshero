from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)