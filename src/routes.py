import flask
import logging
import os
import sys

from src import app
from src.usecases.start_game import try_to_start_game
from src.usecases.stop_game import try_to_stop_game
from src.usecases.claim import try_to_claim
from src.usecases.high_score import try_to_get_high_score, _get_winner

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


@app.route('/', methods=['POST'])
def index():
    return main(flask.request)


def main(request):
    method = request.form['text']
    if method == 'start':
        LOGGER.debug('START REQUEST: \n%s', str(request.form))
        response = try_to_start_game(request.form['channel_id'])
        LOGGER.debug('START RESPONSE: \n%s', str(response))
        return response
    elif method == 'stop':
        LOGGER.debug('STOP REQUEST: \n%s', str(request.form))
        high_score = try_to_get_high_score(request.form['channel_id'])
        winners, score = _get_winner(high_score)
        response = present_winner(winners, score)
        try_to_stop_game(request.form['channel_id'])
        LOGGER.debug('STOP RESPONSE: \n%s', str(response))
        return response
    elif method == 'claim':
        LOGGER.debug('CLAIM REQUEST: \n%s', str(request.form))
        response = try_to_claim(request.form['user_name'],
                                request.form['channel_id'])
        LOGGER.debug('CLAIM RESPONSE: \n%s', str(response))
        return response
    elif method == 'high_score':
        LOGGER.debug('HIGH_SCORE REQUEST: \n%s', str(request.form))
        response = try_to_get_high_score(request.form['channel_id'])
        LOGGER.debug('HIGH_SCORE RESPONSE: \n%s', str(response))
        return response
    else:
        LOGGER.warning('Invalid method: %s', str(request.form))
        return 'You tried to use an invalid method {0}'.format(method)


def present_winner(best_users, highest_score):
    if not best_users:
        return 'No one won :('
    elif len(best_users) > 1:
        map(lambda u: u.user_name, best_users)
        return 'The winners with {0} points are:\n{1}'.format(
            highest_score, '\n'.join(best_users))
    else:
        return 'The winner with {0} points is {1}'.format(
            highest_score, best_users[0].user_name)
