import datetime
import logging
import os
import sys

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
    high_score = {}
    for claim in claims:
        if claim.user in high_score.keys():
            high_score[claim.user] = high_score[claim.user] + 1
        else:
            high_score[claim.user] = 1
    high_score = _sort_high_score(high_score)

    LOGGER.debug("Computed high_score: \n %s", high_score)
    return high_score


def _sort_high_score(high_score):
    winner_to_loser = sorted(
        high_score.keys(), key=lambda user: high_score[user], reverse=True
    )
    sorted_high_score = {}
    for user in winner_to_loser:
        sorted_high_score[user] = high_score[user]
    return sorted_high_score


def _get_winner(high_score):
    highest_score = 0
    best_users = []

    for user_name, score in high_score.items():
        if score > highest_score:
            highest_score = score
            best_users = [get_user(user_name)]
        elif score == highest_score:
            best_users.append(get_user(user_name))
    return best_users, highest_score
