import hmac
import hashlib
import os


def verify_request(version_number, headers, request_body):
    message = "{0}:{1}:{2}".format(
        version_number, headers["X-Slack-Request-Timestamp"], request_body
    )
    slack_signing_secret = bytes(os.environ["SLACK_SIGNING_SECRET"], "utf8")

    hashed_message = (
        version_number
        + "="
        + hmac.new(slack_signing_secret, bytes(message, "utf8"), "sha256").hexdigest()
    )

    print(hashed_message)

    return hashed_message == headers["X-Slack-Signature"]
