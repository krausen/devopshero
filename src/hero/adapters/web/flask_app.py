from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import logging
import os
import sys

from hero.adapters.web.config import Config


LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)

app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=["POST"])
def index():
    return str(main(request.form))


@app.route("/claim", methods=["POST"])
def claim():
    from hero.core import claim

    return str(claim(request.form))


def main(request):
    from hero.core import start, stop, claim, high_score

    method = request["text"]
    try:
        if method == "start":
            return start(request)
        elif method == "stop":
            return stop(request)
        elif method == "high_score":
            return high_score(request)
        else:
            LOGGER.warning("Invalid method: %s", str(request))
            return "You tried to use an invalid method {0}".format(method)
    except Exception as e:
        LOGGER.error(str(e))
