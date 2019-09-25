import datetime
import logging
import os
import sys
from src import db
from src.models import User, Channel, Claim
from src.serializer import create_user, create_channel, create_claim

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def try_to_claim(user_name, channel_id):
    user = User.query.filter_by(user_name=user_name).first()
    if user is None:
        user = create_user(user_name)
    channel = Channel.query.filter_by(channel_id=channel_id).first()
    if channel is None:
        channel = create_channel(channel_id)
    create_claim(datetime.datetime.now(), user.id, channel.id)
    db.session.commit()
    return "Successful claim"


def try_to_start_game(channel_id):
    channel = Channel.query.filter_by(channel_id=channel_id).first()
    if channel is None:
        channel = create_channel(channel_id)
        LOGGER.info('Channel created: %s', channel)
    try:
        LOGGER.info('Starting game in %s', channel)
        return _start_game(channel)
    except Exception as e:
        LOGGER.error(str(e))
        return 'ERROR'


def try_to_stop_game(channel_id):
    channel = Channel.query.filter_by(channel_id=channel_id).first()
    LOGGER.info('Try to stop game in channel: %s', channel)
    try:
        return _stop_game(channel)
    except Exception as e:
        LOGGER.error(str(e))
        return 'ERROR'


def try_to_get_high_score(channel_id):
    channel = Channel.query.filter_by(channel_id=channel_id).first()
    LOGGER.info('Try to get high_score for channel: %s', channel)
    try:
        return _get_high_score(channel)
    except Exception as e:
        LOGGER.error(str(e))
        return 'ERROR'


def _start_game(channel):
    if channel.start:
        LOGGER.warning('Game has already started in %s', channel)
        raise Exception('Game has already started')
    now = datetime.datetime.now().isoformat()
    channel.start = now
    db.session.commit()
    LOGGER.info('Game started at %s', now)
    return "Game has started"


def _stop_game(channel):
    if not channel:
        raise Exception('No such channel')
    elif not channel.start:
        raise Exception('No game started in channel')
    return _finish_game(channel)


def _finish_game(channel):
    high_score = _get_high_score(channel)
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


def _get_high_score(channel, sorted=False):
    claims = Claim.query.filter(Claim.channel_id == channel.id).filter(
        Claim.time >= channel.start).all()
    LOGGER.debug('Compute high_score from claims:\n%s', claims)
    high_score = {}
    for claim in claims:
        user_name = User.query.get(claim.user_id).user_name
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
