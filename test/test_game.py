from datetime import datetime
from unittest import mock
from pytest import raises

from src.game import _compute_the_winner, _stop_game, _start_game

def mock_query_user(user_id):
  mock_user = mock.Mock()
  if user_id is 1:
    mock_user.id = 1
    mock_user.user_name = 'a'
  elif user_id is 2:
    mock_user.id = 2
    mock_user.user_name = 'b'
  return mock_user

@mock.patch('src.game.User')
def test_compute_winner_single_winner(mock_user):
  mock_user.query.get.side_effect = mock_query_user
  mock_claim_a = mock.Mock()
  mock_claim_b = mock.Mock()
  mock_claim_a.user_id = 1
  mock_claim_b.user_id = 1
  mock_claims = [mock_claim_a, mock_claim_b]

  result = _compute_the_winner(mock_claims)

  assert result == 'The winner with 2 points is a'

@mock.patch('src.game.User')
def test_compute_winner_equal(mock_user):
  mock_user.query.get.side_effect = mock_query_user
  mock_claim_a = mock.Mock()
  mock_claim_b = mock.Mock()
  mock_claim_a.user_id = 1
  mock_claim_b.user_id = 2
  mock_claims = [mock_claim_a, mock_claim_b]

  result = _compute_the_winner(mock_claims)

  assert result == 'The winners with 1 points are:\na\nb'


@mock.patch('src.game.User')
def test_compute_winner_no_winner(mock_user):
  result = _compute_the_winner([])

  assert result == 'No one won :('

@mock.patch('src.game.db')
def test_start_game(mock_db):
  mock_channel = mock.Mock()
  mock_channel.start = None

  _start_game(mock_channel)

  assert mock_db.session.commit.called_once()

def test_start_game_already_started():
  mock_channel = mock.Mock()
  mock_channel.start = datetime.now()
  with raises(Exception):
    _start_game(mock_channel)

@mock.patch('src.game._summarize_game')
def test_stop_game_succesfuly(mock_summarize_game):
  mock_channel = mock.Mock()
  mock_channel.start = mock.Mock()

  _stop_game(mock_channel)

  assert mock_summarize_game.called_once_with(mock_channel)


def test_stop_game_none_channel():
  with raises(Exception):
    try_to_stop_game(channel=None)

def test_stop_game_when_game_is_not_started():
  mock_channel = mock.Mock()
  mock_channel.start = None
  with raises(Exception):
    try_to_stop_game(channel=mock_channel)
