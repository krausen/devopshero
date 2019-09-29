import datetime
import logging
import os
import sys

from src.adapters.data_gateway import get_user, get_channel, get_claims_after, channel_exist

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_get_high_score(channel_id):
    LOGGER.info('Try to stop game in channel: %s', channel_id)
    try:
        return _get_high_score(channel_id)
    except Exception as e:
        LOGGER.error(str(e))
        return 'ERROR'


def _get_high_score(channel_id):
    if not channel_exist(channel_id):
        raise Exception('No such channel exist')
    claims = get_claims_after(channel_id, get_channel(channel_id).start)
    LOGGER.debug('Compute high_score from claims:\n%s', claims)
    high_score = {}
    for claim in claims:
        user_name = get_user(claim.user.user_name).user_name
        if user_name in high_score.keys():
            high_score[user_name] = high_score[user_name] + 1
        else:
            high_score[user_name] = 1
    high_score = _sort_high_score(high_score)

    LOGGER.debug('Computed high_score: \n %s', high_score)
    return high_score


def _sort_high_score(high_score):
    winner_to_loser = sorted(high_score.keys(),
                             key=lambda user: high_score[user],
                             reverse=True)
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
