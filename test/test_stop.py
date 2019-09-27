from unittest import mock, TestCase

from src.entities.channel import Channel
from src.usecases.stop_game import try_to_stop_game


@mock.patch('src.usecases.stop_game.stop_game')
@mock.patch('src.usecases.stop_game.game_is_running')
@mock.patch('src.usecases.stop_game.channel_exist')
def test_try_to_start_game(mock_channel_exist, mock_game_is_running,
                           mock_stop_game):
    mock_channel_exist.return_value = True
    mock_game_is_running.return_value = True
    mock_channel = Channel(channel_id='channel_id')
    mock_stop_game.return_value = mock_channel

    channel = try_to_stop_game('mock_channel_id')

    assert channel == mock_channel
