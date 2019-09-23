import unittest.mock as mock

from src.routes import main

@mock.patch('src.routes.game', auto_spec=True)
def test_high_score(mock_game):
  mock_request = mock.Mock()
  mock_request.form = {'text': 'high_score', 'channel_id': 'mock_channel_id'}
  
  main(mock_request)
  
  mock_game.try_to_get_high_score.assert_called_once_with('mock_channel_id')

@mock.patch('src.routes.game', auto_spec=True)
def test_start(mock_game):
  mock_request = mock.Mock()
  mock_request.form = {'text': 'start', 'channel_id': 'mock_channel_id'}
  
  main(mock_request)
  
  mock_game.try_to_start_game.assert_called_once_with('mock_channel_id')

@mock.patch('src.routes.game', auto_spec=True)
def test_stop(mock_game):
  mock_request = mock.Mock()
  mock_request.form = {'text': 'stop', 'channel_id': 'mock_channel_id'}
  
  main(mock_request)
  
  mock_game.try_to_stop_game.assert_called_once_with('mock_channel_id')

@mock.patch('src.routes.game', auto_spec=True)
def test_claim(mock_game):
  mock_request = mock.Mock()
  mock_request.form = {'text': 'claim', 'channel_id': 'mock_channel_id', 'user_name': 'mock_user_name'}
  
  main(mock_request)
  
  mock_game.try_to_claim.assert_called_once_with('mock_user_name', 'mock_channel_id')

@mock.patch('src.routes.game', auto_spec=True)
def test_claim(mock_game):
  mock_request = mock.Mock()
  mock_request.form = {'text': 'mock_invalid_method', 'channel_id': 'mock_channel_id', 'user_name': 'mock_user_name'}
  
  main(mock_request)

  mock_game.try_to_start_game.assert_not_called()
  mock_game.try_to_stop_game.assert_not_called()
  mock_game.try_to_claim.assert_not_called()
  mock_game.try_to_get_high_score.assert_not_called()
