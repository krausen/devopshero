from flask import Flask
from src.adapters.web.config import Config

app = Flask(__name__)
app.config.from_object(Config)
