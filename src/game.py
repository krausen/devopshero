import datetime
from src import db
from src.models import User, Channel, Claim
from src.serializer import create_user, create_channel, create_claim

  
def try_to_claim(user_name, channel_id):
  user = User.query.filter_by(user_name=user_name).first()
  if user is None:
    user = create_user(user_name)
  channel = Channel.query.filter_by(channel_id=channel_id).first()
  if channel is None:
    channel = create_channel(channel_id)
  create_claim(datetime.datetime.now(), user.id, channel.id)
  db.session.commit()


def try_to_start_game(channel_id):
  channel = Channel.query.filter_by(channel_id=channel_id).first()
  if channel is None:
    channel = create_channel(channel_id)
  try:
    return _start_game(channel)
  except Exception as e:
    return str(e)


def try_to_stop_game(channel_id):
  channel = Channel.query.filter_by(channel_id=channel_id).first()
  try:
    return _stop_game(channel)
  except Exception as e:
    return str(e)


def _start_game(channel):
  if not channel.start is None:
    raise Exception('Game has already started')
  channel.start = datetime.datetime.now()
  db.session.commit()
  return "Game has started"


def _stop_game(channel):
  if not channel:
    raise Exception('No such channel')
  elif not channel.start:
    raise Exception('No game started in channel')
  return _summarize_game(channel)


def _summarize_game(channel):
  claims = Claim.query.filter(Claim.channel_id == channel.id).filter(Claim.time >= channel.start).all()
  channel.start = None
  db.session.commit()
  result = _compute_the_winner(claims)
  return result


def _compute_the_winner(claims):
  high_score = _get_high_score(claims)
  highest_score = 0
  best_users = []

  for user, score in high_score.items():
    if score > highest_score:
      highest_score = score
      best_users = [User.query.get(user).user_name]
    elif score == highest_score:
      best_users.append(User.query.get(user).user_name)

  result = _get_game_status(highest_score, best_users)
  return result


def _get_high_score(claims):
  high_score = {}
  for claim in claims:
    if claim.user_id in high_score.keys():
      high_score[claim.user_id] = high_score[claim.user_id] + 1
    else:
      high_score[claim.user_id] = 1
  return high_score


def _get_game_status(highest_score, best_users):
  if not best_users:
    return 'No one won :('
  elif len(best_users) > 1:
    return 'The winners with {0} points are:\n{1}'.format(highest_score, '\n'.join(best_users))
  else:
    return 'The winner with {0} points is {1}'.format(highest_score, best_users[0])
