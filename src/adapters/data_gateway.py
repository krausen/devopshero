from src.adapters.db import db
from src.adapters.db.models import UserModel, ChannelModel, ClaimModel
from src.entities.user import User
from src.entities.channel import Channel
from src.entities.claim import Claim


def get_user(user_name):
    user_model = UserModel.query.filter_by(user_name=user_name).first()
    return User(user_model.user_name)


def get_channel(channel_id):
    channel_model = ChannelModell.query.filter_by(channel_id=channel_id).first()
    return Channel(channel_model.channel_id, channel_model.start)


def get_claims_after(channel_id, time):
    channel_model = ChannelModel.query.filter_by(channel_id=channel_id).first()
    claim_models = ClaimModel.query.filter(
        ClaimModel.channel_id == channel_model.id).filter(
            ClaimModel.time >= time).all()

    claims = []
    for claim in claim_models:
        user_model = UserModel.get(claim.user_id)
        user = User(user_model.user_name)
        channel = Channel(channel_model.channel_id, channel_model.start)
        claims.append(Claim(claim_model.time, user, channel))
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
    claim_model = ClaimModel(time=time,
                             user_id=user.id,
                             channel_id=channel_model.id)
    db.session.add(claim_model)
    db.session.commit()
    user = User(user_name)
    channel = Channel(channel_id)
    return Claim(claim_model.time, user, channel)


def start_game(channel_id, time):
    user = get_channel(channel_id)
    channel.start = time
    db.session.commit()


def stop_game(channel_id):
    channel = get_channel(channel_id)
    channel.start = None
    db.session.commit()


def channel_exist(channel_id):
    channel = get_channel(channel_id)
    return channel != None


def user_exist(user_name):
    user = get_user(user_name)
    return user != None


def game_is_running(channel_id):
    channel = get_channel(channel_id)
    return channel.start != None
