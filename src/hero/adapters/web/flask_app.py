from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
import logging
import os
import sys

from hero.adapters.web.config import Config
from hero.adapters.slack.verify_request import verify_request


LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)

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
    if not verify_request("v0", request.headers, request.data):
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
        LOGGER.warning("Invalid method: %s", str(request))
        return "You tried to use an invalid method {0}".format(method)
