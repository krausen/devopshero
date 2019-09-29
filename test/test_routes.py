import unittest.mock as mock

from src.entities.user import User
from src.request import start, stop, claim, high_score, present_winner


@mock.patch('src.request.try_to_get_high_score')
def test_high_score(try_to_get_high_score):
    mock_request = {'text': 'high_score', 'channel_id': 'mock_channel_id'}

    high_score(mock_request)

    try_to_get_high_score.assert_called_once_with('mock_channel_id')


@mock.patch('src.request.try_to_start_game')
def test_start(try_to_start_game):
    mock_request = {'text': 'start', 'channel_id': 'mock_channel_id'}

    start(mock_request)

    try_to_start_game.assert_called_once_with('mock_channel_id')


@mock.patch('src.request._get_winner')
@mock.patch('src.request.try_to_get_high_score')
@mock.patch('src.request.try_to_stop_game')
def test_stop(try_to_stop_game, mock_try_to_get_high_score, mock_get_winner):
    mock_request = {'text': 'stop', 'channel_id': 'mock_channel_id'}
    mock_try_to_get_high_score.return_value = {'user_a': 3, 'user_b': 1}
    mock_get_winner.return_value = [User('user_a')], 3

    response = stop(mock_request)

    assert response == 'The winner with 3 points is user_a'


@mock.patch('src.request.try_to_claim')
def test_claim(try_to_claim):
    mock_request = {
        'text': 'claim',
        'channel_id': 'mock_channel_id',
        'user_name': 'mock_user_name'
    }

    claim(mock_request)

    try_to_claim.assert_called_once_with('mock_user_name', 'mock_channel_id')


def test_present_winner_no_winner():
    best_user = []
    highest_score = 0

    response = present_winner(best_user, highest_score)

    assert response == 'No one won :('


def test_present_winner_two_winners():
    best_user = [User('user_a'), User('user_b')]
    highest_score = 1

    response = present_winner(best_user, highest_score)

    assert response == 'The winners with 1 points are:\nuser_a\nuser_b'
