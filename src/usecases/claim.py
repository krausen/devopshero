import datetime
import logging
import os
import sys
from src.repositories.data_gateway import create_user, create_channel, create_claim, channel_exist, user_exist

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_claim(user_name, channel_id):
    if not user_exist(user_name):
        create_user(user_name)
    if not channel_exist(channel_id):
        create_channel(channel_id)
    claim = create_claim(datetime.datetime.now(), user_name, channel_id)
    return claim
