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

    
    message = "v0:".encode("utf8") + time_stamp + ":".encode("utf8") + request.data

    LOGGER.debug(message)
    LOGGER.debug(time_stamp)
    hashed_message = (
        "v0="
        + hmac.new(slack_signing_secret, message, "sha256").hexdigest()
    )

    LOGGER.debug(hashed_message)

    return hmac.compare_digest(hashed_message, request.headers["X-Slack-Signature"])
