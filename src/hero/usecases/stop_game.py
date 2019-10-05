import logging
import os
import sys
from hero.adapters.data_gateway import channel_exist, game_is_running, stop_game

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_stop_game(channel_id):
    LOGGER.info("Try to stop game in channel: %s", channel_id)
    if not channel_exist(channel_id):
        LOGGER.warning("No such channel")
        raise Exception("No such channel")
    elif not game_is_running(channel_id):
        LOGGER.warning("No game is running")
        raise Exception("No game started in channel")
    LOGGER.debug("Stop game %s", channel_id)
    stop_game(channel_id)
