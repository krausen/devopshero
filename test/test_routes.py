import unittest.mock as mock

from src.entities.user import User
from src.routes import main


@mock.patch('src.routes.try_to_get_high_score')
def test_high_score(try_to_get_high_score):
    mock_request = mock.Mock()
    mock_request.form = {'text': 'high_score', 'channel_id': 'mock_channel_id'}

    main(mock_request)

    try_to_get_high_score.assert_called_once_with('mock_channel_id')


@mock.patch('src.routes.try_to_start_game')
def test_start(try_to_start_game):
    mock_request = mock.Mock()
    mock_request.form = {'text': 'start', 'channel_id': 'mock_channel_id'}

    main(mock_request)

    try_to_start_game.assert_called_once_with('mock_channel_id')


@mock.patch('src.routes._get_winner')
@mock.patch('src.routes.try_to_get_high_score')
@mock.patch('src.routes.try_to_stop_game')
def test_stop(try_to_stop_game, mock_try_to_get_high_score, mock_get_winner):
    mock_request = mock.Mock()
    mock_request.form = {'text': 'stop', 'channel_id': 'mock_channel_id'}
    mock_try_to_get_high_score.return_value = {'user_a': 3, 'user_b': 1}
    mock_get_winner.return_value = [User('user_a')], 3

    response = main(mock_request)

    assert response == 'The winner with 3 points is user_a'


@mock.patch('src.routes.try_to_claim')
def test_claim(try_to_claim):
    mock_request = mock.Mock()
    mock_request.form = {
        'text': 'claim',
        'channel_id': 'mock_channel_id',
        'user_name': 'mock_user_name'
    }

    main(mock_request)

    try_to_claim.assert_called_once_with('mock_user_name', 'mock_channel_id')


@mock.patch('src.routes.try_to_start_game')
@mock.patch('src.routes.try_to_stop_game')
@mock.patch('src.routes.try_to_claim')
@mock.patch('src.routes.try_to_get_high_score')
def test_invalid_method(try_to_start_game, try_to_stop_game, try_to_claim,
                        try_to_get_high_score):
    mock_request = mock.Mock()
    mock_request.form = {
        'text': 'mock_invalid_method',
        'channel_id': 'mock_channel_id',
        'user_name': 'mock_user_name'
    }

    main(mock_request)

    try_to_start_game.assert_not_called()
    try_to_stop_game.assert_not_called()
    try_to_claim.assert_not_called()
    try_to_get_high_score.assert_not_called()
