from src.request import start, stop, claim, high_score


@app.route("/", methods=["POST"])
def index():
    return main(flask.request.form)


@app.route("/claim", methods=["POST"])
def claim():
    return high_score(flask.request.form)


def main(request):
    method = request["text"]
    if method == "start":
        return start(request)
    elif method == "stop":
        return stop(request)
    elif method == "high_score":
        return high_score(request)
    else:
        LOGGER.warning("Invalid method: %s", str(request))
        return "You tried to use an invalid method {0}".format(method)
