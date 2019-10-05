from hero.adapters.db.models import User as UserModel
from hero.adapters.db.models import Channel as ChannelModel
from hero.adapters.db.models import Claim as ClaimModel
from hero.adapters.db.models import db
from hero.entities.user import User
from hero.entities.channel import Channel
from hero.entities.claim import Claim
import logging
import os
import sys

LOGGER = logging.getLogger(__name__)
sh = logging.StreamHandler(stream=sys.stdout)
LOGGER.setLevel(os.environ.get("LOGLEVEL", "INFO"))
LOGGER.addHandler(sh)


def get_user(user_name):
    user_model = UserModel.query.filter_by(user_name=user_name).first()
    if user_model:
        return User(user_model.user_name)


def get_channel(channel_id):
    LOGGER.debug("get_channel(%s)", channel_id)
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    LOGGER.debug("get_channel(%s)=%s", channel_id, channel_model)
    if channel_model:
        return Channel(channel_model.channel_id, channel_model.start)
    return None


def get_claims_after_start(channel_id):
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    claim_models = (
        ClaimModel.query.filter(ClaimModel.channel_id == channel_model.id)
        .filter(ClaimModel.time >= channel_model.start)
        .all()
    )

    claims = []
    for claim in claim_models:
        user_model = UserModel.query.get(claim.user_id)
        user = User(user_model.user_name)
        channel = Channel(channel_model.channel_id, channel_model.start)
        claims.append(Claim(claim.time, user, channel))
    return claims


def create_user(user_name):
    user_model = UserModel(user_name=user_name)
    db.session.add(user_model)
    db.session.commit()
    return User(user_model.user_name)


def create_channel(channel_id):
    channel_model = ChannelModel(channel_id=channel_id)
    db.session.add(channel_model)
    db.session.commit()
    return Channel(channel_model.channel_id, channel_model.start)


def create_claim(time, user_name, channel_id):
    user_model = UserModel.query.filter_by(user_name=user_name).first()
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    claim_model = ClaimModel(
        time=time, user_id=user_model.id, channel_id=channel_model.id
    )
    db.session.add(claim_model)
    db.session.commit()
    user = User(user_name)
    channel = Channel(channel_id)
    return Claim(claim_model.time, user, channel)


def start_game(channel_id, time):
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    if channel_model:
        channel_model.start = time
        db.session.commit()
    return channel_model


def stop_game(channel_id):
    # LOGGER.debug('stop_game(%s)', channel_id)
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    if channel_model:
        channel_model.start = None
        db.session.commit()
    # LOGGER.debug('stop_game(%s)=Done', channel_model)
    return channel_model


def channel_exist(channel_id):
    LOGGER.debug("channel_exist(%s)", channel_id)
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    channel_exist = bool(channel_model)
    LOGGER.debug("channel_exist(%s)=%s", channel_id, channel_exist)
    return channel_exist


def user_exist(user_name):
    user = UserModel.query.filter_by(user_name=user_name).first()
    return bool(user)


def game_is_running(channel_id):
    LOGGER.debug("game_is_running")
    LOGGER.debug("game_is_running(%s)", channel_id)
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    game_is_running = bool(channel_model.start)
    LOGGER.debug("game_is_running(%s)=%s", channel_id, game_is_running)
    return game_is_running
