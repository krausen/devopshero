import os


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "..", "db", "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
