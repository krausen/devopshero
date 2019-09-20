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
