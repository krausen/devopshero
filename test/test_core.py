import unittest.mock as mock

from hero.entities.user import User
from hero.core import start, stop, claim, high_score, present_winner, present_high_score


@mock.patch("hero.core.try_to_get_high_score")
def test_high_score(try_to_get_high_score):
    mock_request = {"text": "high_score", "channel_id": "mock_channel_id"}

    high_score(mock_request)

    try_to_get_high_score.assert_called_once_with("mock_channel_id")


@mock.patch("hero.core.try_to_start_game")
def test_start(try_to_start_game):
    mock_request = {"text": "start", "channel_id": "mock_channel_id"}

    start(mock_request)

    try_to_start_game.assert_called_once_with("mock_channel_id")


@mock.patch("hero.core._get_winner")
@mock.patch("hero.core.try_to_get_high_score")
@mock.patch("hero.core.try_to_stop_game")
def test_stop(mock_try_to_stop_game, mock_try_to_get_high_score, mock_get_winner):
    mock_request = {"text": "stop", "channel_id": "mock_channel_id"}
    mock_try_to_get_high_score.return_value = {"user_a": 3, "user_b": 1}
    mock_get_winner.return_value = [User("user_a")], 3

    response = stop(mock_request)

    mock_try_to_stop_game.assert_called_once_with("mock_channel_id")


@mock.patch("hero.core.try_to_claim")
def test_claim(try_to_claim):
    mock_request = {
        "text": "claim",
        "channel_id": "mock_channel_id",
        "user_name": "mock_user_name",
    }

    claim(mock_request)

    try_to_claim.assert_called_once_with("mock_user_name", "mock_channel_id")


def test_present_winner_no_winner():
    best_user = []
    highest_score = 0

    response = present_winner({})

    assert response == "No one won :("


def test_present_winner_two_winners():
    user_a = User("user_a")
    user_b = User("user_b")
    best_user = [user_a, user_b]
    highest_score = 1
    high_score = {user_a: 1, user_b: 1}

    response = present_winner(high_score)

    print(response)
    assert (
        response
        == "The winners with 1 points are:\nuser_a\nuser_b\n{user_a: 1, user_b: 1}"
    )


def test_present_high_score():
    user_a = User("user_a")
    user_b = User("user_b")
    high_score = {user_a: 1, user_b: 1}

    presentable_high_score = present_high_score(high_score)

    assert presentable_high_score == {"user_a": 1, "user_b": 1}
