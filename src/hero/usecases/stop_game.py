import logging
import os
import sys
from hero.adapters.data_gateway import (
    channel_exist,
    game_is_running,
    get_channel,
    stop_game,
)

LOGGER = logging.getLogger(__name__)


def try_to_stop_game(channel_id):
    LOGGER.info("Try to stop game in channel: %s", channel_id)
    if not channel_exist(channel_id):
        LOGGER.info("No such channel")
        return
    elif not game_is_running(channel_id):
        LOGGER.info("No game is running")
        return get_channel(channel_id)
    channel = stop_game(channel_id)
    return channel
