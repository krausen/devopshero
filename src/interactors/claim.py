import datetime
import logging
import os
import sys
from src.data_gateway import create_user, create_channel, create_claim, channel_exist, user_exist

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_claim(user_name, channel_id):
    if not user_exist(user_name):
        user = create_user(user_name)
    if not channel_exist(channel_id):
        create_channel(channel_id)
    create_claim(datetime.datetime.now(), user.id, channel.id)
    return "Successful claim"
