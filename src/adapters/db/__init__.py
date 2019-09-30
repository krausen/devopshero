from flask_sqlalchemy import SQLAlchemy
from src.adapters.web import app

db = SQLAlchemy(app)
