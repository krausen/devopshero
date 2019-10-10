import datetime
import logging
import os
import sys
from hero.adapters.data_gateway import (
    create_channel,
    channel_exist,
    game_is_running,
    start_game,
)

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_start_game(channel_id):
    LOGGER.info("Trying to start game in channel %s", channel_id)
    if not channel_exist(channel_id):
        create_channel(channel_id)
        LOGGER.info("Channel created with id: %s", channel_id)
    if game_is_running(channel_id):
        LOGGER.warning("Game has already started in %s", channel_id)
        raise Exception("Game has already started")
    LOGGER.info("Starting game in %s", channel_id)
    now = datetime.datetime.now()
    channel = start_game(channel_id, now)
    LOGGER.info("Game started in %s at %s", channel_id, now)
    return not channel.start == None
