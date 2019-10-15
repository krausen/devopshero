import datetime
import logging
import os
import sys

from hero.entities.high_score import HighScore
from hero.adapters.data_gateway import (
    get_user,
    get_channel,
    get_claims_after_start,
    channel_exist,
    game_is_running,
)

LOGGER = logging.getLogger(__name__)


def try_to_get_high_score(channel_id):
    LOGGER.info("Try to get high score from channel: %s", channel_id)
    if not channel_exist(channel_id):
        LOGGER.info("No such channel exist %s", channel_exist)
        return
    if not game_is_running(channel_id):
        LOGGER.info("No game running in %s", channel_exist)
        return
    claims = get_claims_after_start(channel_id)
    high_score = HighScore()
    for claim in claims:
        high_score.add(claim.user)
    high_score.sort()

    return high_score
