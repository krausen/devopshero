import hmac
import hashlib
import os
import logging
import os
import sys

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def verify_request(request):
    time_stamp = request.headers["X-Slack-Request-Timestamp"].encode("utf8")
    slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"].encode("utf8")

    message = b"v0:%b:%b" % (time_stamp, request.data)

    hashed_message = (
        "v0=" + hmac.new(slack_signing_secret, message, hashlib.sha256).hexdigest()
    )

    LOGGER.debug(message)
    if hmac.compare_digest(hashed_message, request.headers["X-Slack-Signature"]):
        LOGGER.info("Request verified: \n%s \n%s", request.headers, request.data)
        return True
    else:
        LOGGER.warning("Unauthorized request: \n%s \n%s", request.headers, request.data)
        return False
