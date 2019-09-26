import datetime
import logging
import os
import sys
from src.data_gateway import create_user, create_channel, create_claim, channel_exist, game_is_running, start_game, get_user, get_channel, user_exist

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_claim(user_name, channel_id):
    if not user_exist(user_name):
        user = create_user(user_name)
    if not channel_exist(channel_id):
        create_channel(channel_id)
    create_claim(datetime.datetime.now(), user.id, channel.id)
    return "Successful claim"


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


def try_to_stop_game(channel_id):
    LOGGER.info('Try to stop game in channel: %s', channel_id)
    try:
        return _stop_game(channel_id)
    except Exception as e:
        LOGGER.error(str(e))
        return 'ERROR'


def try_to_get_high_score(channel_id):
    LOGGER.info('Try to get high_score for channel: %s', channel_id)
    try:
        return _get_high_score(channel_id)
    except Exception as e:
        LOGGER.error(str(e))
        return 'ERROR'


def _start_game(channel_id):
    if game_is_running(channel_id):
        LOGGER.warning('Game has already started in %s', channel_id)
        raise Exception('Game has already started')
    now = datetime.datetime.now().isoformat()
    start_game(channel_id, now)
    LOGGER.info('Game started in %s at %s', channel_id, now)
    return "Game has started"


def _stop_game(channel_id):
    if not channel_exist(channel_id):
        raise Exception('No such channel')
    elif not game_is_running(channel_id):
        raise Exception('No game started in channel')
    return _finish_game(channel_id)


def _finish_game(channel_id):
    high_score = _get_high_score(channel_id)
    channel.start = None
    LOGGER.debug('Computed high_score: \n %s', high_score)
    highest_score = 0
    best_users = []

    for user_name, score in high_score.items():
        if score > highest_score:
            highest_score = score
            best_users = [user_name]
        elif score == highest_score:
            best_users.append(user_name)

    result = _get_winner(highest_score, best_users)
    db.session.commit()
    return result


def _get_high_score(channel_id, sorted=False):
    claims = get_claims_after(channel_id, get_channel(channel_id).start)
    LOGGER.debug('Compute high_score from claims:\n%s', claims)
    high_score = {}
    for claim in claims:
        user_name = get_user(claim.user_id).user_name
        if user_name in high_score.keys():
            high_score[user_name] = high_score[user_name] + 1
        else:
            high_score[user_name] = 1
    if sorted:
        high_score = _sort_high_score(high_score)
    return high_score


def _sort_high_score(high_score):
    winner_to_loser = sorted(high_score.keys(),
                             key=lambda user: high_score[user],
                             reverse=True)
    sorted_high_score = {}
    for user in winner_to_loser:
        sorted_high_score[user] = high_score[user]
    return sorted_high_score


def _get_winner(highest_score, best_users):
    if not best_users:
        return 'No one won :('
    elif len(best_users) > 1:
        return 'The winners with {0} points are:\n{1}'.format(
            highest_score, '\n'.join(best_users))
    else:
        return 'The winner with {0} points is {1}'.format(
            highest_score, best_users[0])
