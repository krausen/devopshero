from unittest import mock, TestCase

from hero.entities.channel import Channel
from hero.usecases.stop_game import try_to_stop_game


@mock.patch("hero.usecases.stop_game.stop_game")
@mock.patch("hero.usecases.stop_game.game_is_running")
@mock.patch("hero.usecases.stop_game.channel_exist")
def test_try_to_start_game(mock_channel_exist, mock_game_is_running, mock_stop_game):
    mock_channel_exist.return_value = True
    mock_game_is_running.return_value = True
    mock_channel = Channel(channel_id="channel_id")
    mock_stop_game.return_value = mock_channel

    channel = try_to_stop_game("mock_channel_id")

    mock_stop_game.assert_called_once_with("mock_channel_id")


@mock.patch("hero.usecases.stop_game.stop_game")
@mock.patch("hero.usecases.stop_game.game_is_running")
@mock.patch("hero.usecases.stop_game.channel_exist")
def test_try_to_start_game_no_channel(
    mock_channel_exist, mock_game_is_running, mock_stop_game
):
    mock_channel_exist.return_value = False
    mock_game_is_running.return_value = False

    try:
        try_to_stop_game("mock_channel_id")
    except Exception as e:
        assert str(e) == "No such channel"


@mock.patch("hero.usecases.stop_game.stop_game")
@mock.patch("hero.usecases.stop_game.game_is_running")
@mock.patch("hero.usecases.stop_game.channel_exist")
def test_try_to_start_game_no_game_running(
    mock_channel_exist, mock_game_is_running, mock_stop_game
):
    mock_channel_exist.return_value = True
    mock_game_is_running.return_value = False

    try:
        try_to_stop_game("mock_channel_id")
    except Exception as e:
        assert str(e) == "No game started in channel"
