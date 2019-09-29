import datetime
import logging
import os
import sys
from src.adapters.data_gateway import create_channel, channel_exist, game_is_running, start_game

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_start_game(channel_id):
    if not channel_exist(channel_id):
        create_channel(channel_id)
        LOGGER.info('Channel created with id: %s', channel_id)
    try:
        LOGGER.info('Starting game in %s', channel_id)
        return _start_game(channel_id)
    except Exception as e:
        LOGGER.error(str(e))
        return 'ERROR'


def _start_game(channel_id):
    if game_is_running(channel_id):
        LOGGER.warning('Game has already started in %s', channel_id)
        raise Exception('Game has already started')
    now = datetime.datetime.now().isoformat()
    channel = start_game(channel_id, now)
    LOGGER.info('Game started in %s at %s', channel_id, now)
    return channel
