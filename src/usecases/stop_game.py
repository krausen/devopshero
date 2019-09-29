import logging
import os
import sys
from src.adapters.data_gateway import channel_exist, game_is_running, stop_game

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_stop_game(channel_id):
    LOGGER.info('Try to stop game in channel: %s', channel_id)
    try:
        return _stop_game(channel_id)
    except Exception as e:
        LOGGER.error(str(e))
        raise (e)


def _stop_game(channel_id):
    if not channel_exist(channel_id):
        raise Exception('No such channel')
    elif not game_is_running(channel_id):
        raise Exception('No game started in channel')
    channel = stop_game(channel_id)
    return channel
