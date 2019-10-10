import logging
import os
import sys

from hero.usecases.start_game import try_to_start_game
from hero.usecases.stop_game import try_to_stop_game
from hero.usecases.claim import try_to_claim
from hero.usecases.high_score import try_to_get_high_score, _get_winner

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def claim(args):
    return try_to_claim(args["user_name"], args["channel_id"])


def start(args):
    return try_to_start_game(args["channel_id"])
    return response


def stop(args):
    high_score = try_to_get_high_score(args["channel_id"])
    response = present_winner(high_score)
    try_to_stop_game(args["channel_id"])
    return response


def high_score(args):
    high_score = try_to_get_high_score(args["channel_id"])
    return present_high_score(high_score)


def present_high_score(high_score):
    high_score_dict = {}
    for user, score in high_score.items():
        high_score_dict[user.user_name] = score
    return high_score_dict


def present_winner(high_score):
    best_users, highest_score = _get_winner(high_score)
    if not best_users:
        return "No one won :("
    elif len(best_users) > 1:
        best_users = map(lambda u: u.user_name, best_users)
        return "The winners with {0} points are:\n{1}\n{2}".format(
            highest_score, "\n".join(best_users), high_score
        )
    else:
        return "The winner with {0} points is {1}\n{2}".format(
            highest_score, best_users[0].user_name, high_score
        )
