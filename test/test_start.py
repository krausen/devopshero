from datetime import datetime
from unittest import mock, TestCase

from src.entities.channel import Channel
from src.usecases.start_game import try_to_start_game


@mock.patch('src.usecases.start_game.start_game')
@mock.patch('src.usecases.start_game.game_is_running')
@mock.patch('src.usecases.start_game.channel_exist')
def test_try_to_start_game(mock_channel_exist, mock_game_is_running,
                           mock_start_game):
    mock_channel_exist.return_value = True
    mock_game_is_running.return_value = False
    mock_channel = Channel(channel_id='mock_channel_id', start=datetime.now())
    mock_start_game.return_value = mock_channel

    channel = try_to_start_game('mock_channel_id')

    assert channel == mock_channel


@mock.patch('src.usecases.start_game.start_game')
@mock.patch('src.usecases.start_game.game_is_running')
@mock.patch('src.usecases.start_game.create_channel')
@mock.patch('src.usecases.start_game.channel_exist')
def test_try_to_start_game_channel_does_not_exist(mock_channel_exist,
                                                  mock_create_channel,
                                                  mock_game_is_running,
                                                  mock_start_game):
    mock_channel_exist.return_value = False
    mock_game_is_running.return_value = False
    mock_channel = Channel(channel_id='mock_channel_id', start=datetime.now())
    mock_start_game.return_value = mock_channel

    try_to_start_game('mock_channel_id')

    mock_create_channel.assert_called_once_with('mock_channel_id')
    mock_start_game.assert_called_once()


@mock.patch('src.usecases.start_game.start_game')
@mock.patch('src.usecases.start_game.game_is_running')
@mock.patch('src.usecases.start_game.create_channel')
@mock.patch('src.usecases.start_game.channel_exist')
def test_try_to_start_game_already_started(mock_channel_exist,
                                           mock_create_channel,
                                           mock_game_is_running,
                                           mock_start_game):
    mock_channel_exist.return_value = True
    mock_game_is_running.return_value = True
    mock_channel = Channel(channel_id='mock_channel_id', start=datetime.now())
    mock_start_game.return_value = mock_channel

    try:
        try_to_start_game('mock_channel_id')
    except Exception as e:
        assert str(e) == 'Game has already started'
