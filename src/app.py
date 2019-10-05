from flask_migrate import Migrate

from hero.adapters.web.flask_app import app  # This will init the flask app
from hero.adapters.db.models import db  # This will init the db

Migrate(app, db)
