from src import db
from src.models import User, Channel, Claim


def create_user(user_name):
    user = User(user_name=user_name)
    db.session.add(user)
    db.session.commit()
    return user


def create_channel(channel_id):
    channel = Channel(channel_id=channel_id)
    db.session.add(channel)
    db.session.commit()
    return channel


def create_claim(time, user_id, channel_id):
    claim = Claim(time=time, user_id=user_id, channel_id=channel_id)
    db.session.add(claim)
    db.session.commit()
    return claim


def start_game(channel_id, time):
    user = get_channel(channel_id)
    channel.start = time
    db.session.commit()


def channel_exist(channel_id):
    channel = Channel.query.filter_by(channel_id=channel_id).first()
    return channel != None


def user_exist(user_name):
    user = User.query.filter_by(user_name=user_name).first()
    return user != None


def game_is_running(channel_id):
    return channel.start != None


def get_user(user_name):
    return User.query.filter_by(user_name=user_name).first()


def get_channel(channel_id):
    return Channel.query.filter_by(channel_id=channel_id).first()


def get_claims_after(channel_id, time):
    return Claim.query.filter(Claim.channel_id == channel_id).filter(
        Claim.time >= time).all()
