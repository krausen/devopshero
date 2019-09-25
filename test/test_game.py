from unittest import mock
import datetime

from src.game import _sort_high_score, try_to_start_game, try_to_stop_game
from src.models import Channel


@mock.patch('src.game.db')
@mock.patch.object(Channel, 'query', auto_spec=True)
def test_try_to_start_game(mock_channel_query, mock_db):
  channel_mock = mock.Mock()
  channel_mock.start = None
  mock_channel_query.filter_by.return_value.first.return_value = channel_mock

  try_to_start_game('channel_id')
  
  assert channel_mock.start
  mock_db.session.commit.assert_called_once()


@mock.patch('src.game._finish_game')
@mock.patch.object(Channel, 'query', auto_spec=True)
def test_try_to_stop_game(mock_channel_query, mock_finish_game):
  channel_mock = mock.Mock()
  channel_mock.start = datetime.datetime.now()
  mock_channel_query.filter_by.return_value.first.return_value = channel_mock

  try_to_stop_game('channel_id')

  mock_finish_game.assert_called_once_with(channel_mock)


def test_sort_high_score():
  high_score = {'user_a': 3, 'user_b': 4}

  sorted_high_score = _sort_high_score(high_score)

  assert high_score == {'user_b': 4, 'user_a': 3}