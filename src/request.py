import logging
import os
import sys

from src.usecases.start_game import try_to_start_game
from src.usecases.stop_game import try_to_stop_game
from src.usecases.claim import try_to_claim
from src.usecases.high_score import try_to_get_high_score, _get_winner

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def claim(request):
    LOGGER.debug("CLAIM REQUEST: \n%s", str(request))
    response = try_to_claim(request["user_name"], request["channel_id"])
    LOGGER.debug("CLAIM RESPONSE: \n%s", str(response))


def start(request):
    LOGGER.debug("START REQUEST: \n%s", str(request))
    response = try_to_start_game(request["channel_id"])
    LOGGER.debug("START RESPONSE: \n%s", str(response))
    return response


def stop(request):
    LOGGER.debug("STOP REQUEST: \n%s", str(request))
    high_score = try_to_get_high_score(request["channel_id"])
    winners, score = _get_winner(high_score)
    response = present_winner(winners, score)
    try_to_stop_game(request["channel_id"])
    LOGGER.debug("STOP RESPONSE: \n%s", str(response))
    return response


def high_score(request):
    LOGGER.debug("HIGH_SCORE REQUEST: \n%s", str(request))
    response = try_to_get_high_score(request["channel_id"])
    LOGGER.debug("HIGH_SCORE RESPONSE: \n%s", str(response))
    return response


def present_winner(best_users, highest_score):
    if not best_users:
        return "No one won :("
    elif len(best_users) > 1:
        best_users = map(lambda u: u.user_name, best_users)
        return "The winners with {0} points are:\n{1}".format(
            highest_score, "\n".join(best_users)
        )
    else:
        return "The winner with {0} points is {1}".format(
            highest_score, best_users[0].user_name
        )
