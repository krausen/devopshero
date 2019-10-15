import datetime
import logging
import os
import sys
from hero.adapters.data_gateway import (
    create_channel,
    channel_exist,
    game_is_running,
    get_channel,
    start_game,
)

LOGGER = logging.getLogger(__name__)


def try_to_start_game(channel_id):
    LOGGER.info("Trying to start game in channel %s", channel_id)
    if not channel_exist(channel_id):
        create_channel(channel_id)
        LOGGER.info("Channel created with id: %s", channel_id)
    elif game_is_running(channel_id):
        LOGGER.info("Game was already started")
        return get_channel(channel_id)
    LOGGER.info("Starting game in %s", channel_id)
    now = datetime.datetime.now()
    channel = start_game(channel_id, now)
    LOGGER.info("Game started in %s at %s", channel_id, now)
    return channel
