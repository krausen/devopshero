from unittest import mock, TestCase

from hero.entities.user import User
from hero.usecases.high_score import (
    _get_winner,
    _sort_high_score,
    try_to_get_high_score,
)


@mock.patch("hero.usecases.high_score.get_claims_after_start")
@mock.patch("hero.usecases.high_score.game_is_running")
@mock.patch("hero.usecases.high_score.channel_exist")
def test_try_to_get_high_score(
    mock_channel_exist, mock_game_is_running, mock_get_claims_after
):
    user_a = User(user_name="user_a")
    user_b = User(user_name="user_b")
    claim_1 = mock.Mock()
    claim_2 = mock.Mock()
    claim_3 = mock.Mock()
    claim_1.user = user_a
    claim_2.user = user_b
    claim_3.user = user_a
    mock_get_claims_after.return_value = [claim_1, claim_2, claim_3]
    mock_channel_exist.return_value = True
    mock_game_is_running.return_value = True

    high_score = try_to_get_high_score("mock_channel_id")
    assert len(high_score) == 2
    assert high_score == {user_a: 2, user_b: 1}


@mock.patch("hero.usecases.high_score.get_channel")
@mock.patch("hero.usecases.high_score.get_user")
@mock.patch("hero.usecases.high_score.get_claims_after_start")
@mock.patch("hero.usecases.high_score.channel_exist")
def test_try_to_get_high_score_no_channel_exist(
    mock_channel_exist, mock_get_claims_after, mock_get_user, _
):
    mock_channel_exist.return_value = False

    try:
        try_to_get_high_score("mock_channel_id")
    except Exception as e:
        assert str(e) == "No such channel exist"


@mock.patch("hero.usecases.high_score.get_channel")
@mock.patch("hero.usecases.high_score.get_user")
@mock.patch("hero.usecases.high_score.get_claims_after_start")
@mock.patch("hero.usecases.high_score.game_is_running")
@mock.patch("hero.usecases.high_score.channel_exist")
def test_try_to_get_high_score_game_is_started(
    mock_channel_exist, mock_game_is_running, mock_get_claims_after, mock_get_user, _
):
    mock_channel_exist.return_value = True
    mock_game_is_running.return_value = False

    try:
        try_to_get_high_score("mock_channel_id")
    except Exception as e:
        assert str(e) == "No game is running"


def test_sort_high_score():
    high_score = {"user_a": 3, "user_b": 4}

    sorted_high_score = _sort_high_score(high_score)

    assert high_score == {"user_b": 4, "user_a": 3}


@mock.patch("hero.usecases.high_score.get_user")
def test_get_winner(mock_get_user):
    user_a = User("user_a")
    user_b = User("user_b")
    mock_get_user.side_effect = [user_a, user_b]
    high_score = {user_a: 4, user_b: 3}

    winner, score = _get_winner(high_score)

    assert winner == [user_a]
    assert score == 4


@mock.patch("hero.usecases.high_score.get_user")
def test_get_winner_draw(mock_get_user):
    user_a = User("user_a")
    user_b = User("user_b")
    mock_get_user.side_effect = [user_a, user_b]
    high_score = {user_a: 4, user_b: 4}

    winners, score = _get_winner(high_score)

    assert user_a in winners
    assert user_b in winners
    assert len(winners) == 2
    assert score == 4


@mock.patch("hero.usecases.high_score.get_user")
def test_get_winner_no_winner(_):
    high_score = {}

    winners, score = _get_winner(high_score)

    assert score == 0
    assert winners == []
