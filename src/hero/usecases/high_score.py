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
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_get_high_score(channel_id):
    LOGGER.info("Try to get high score from channel: %s", channel_id)
    if not channel_exist(channel_id):
        raise Exception("No such channel exist")
    if not game_is_running(channel_id):
        raise Exception("No game is running")
    claims = get_claims_after_start(channel_id)
    LOGGER.debug("Compute high_score from claims:\n%s", claims)
    high_score = HighScore()
    for claim in claims:
        high_score.add(claim.user)
    high_score.sort()

    LOGGER.debug("Computed high_score: \n %s", high_score)
    return high_score
