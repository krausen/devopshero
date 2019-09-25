from unittest import mock, TestCase
import datetime

from src.game import _sort_high_score, try_to_start_game
from src.models import Channel


class TestGame(TestCase):

  @mock.patch('src.game.db')
  @mock.patch.object(Channel, 'query', auto_spec=True)
  def test_try_to_start_game(self, mock_channel_query, mock_db):
    channel_mock = mock.Mock()
    channel_mock.start = None
    mock_channel_query.filter_by.return_value.first.return_value = channel_mock

    try_to_start_game('channel_id')
    
    assert channel_mock.start
    assert mock_db.session.commit.called_once()


  def test_sort_high_score(self):
    high_score = {'user_a': 3, 'user_b': 4}

    sorted_high_score = _sort_high_score(high_score)

    assert high_score == {'user_b': 4, 'user_a': 3}