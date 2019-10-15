from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import logging
import os
import sys

from hero.adapters.web.config import Config
from hero.adapters.slack.verify_request import verify_request


LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(Config)


@app.route("/", methods=["POST"])
def index():
    return str(main(request))


@app.route("/claim", methods=["POST"])
def claim():
    from hero.core import claim

    return str(claim(request))


def main(request):
    try:
        request.data = request.get_data()
        if not verify_request(request):
            abort(403)

        from hero.core import start, stop, claim, high_score

        method = request.form["text"]
        if method == "start":
            return start(request.form)
        elif method == "stop":
            return stop(request.form)
        elif method == "high_score":
            return high_score(request.form)
        else:
            LOGGER.error("Invalid method: %s", str(request))
            raise ValueError(f"You tried to use an invalid method: {method}")
    except Exception as e:
        LOGGER.error(str(e))
        raise e
