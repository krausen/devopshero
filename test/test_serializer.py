from datetime import datetime
from unittest import mock
from src.serializer import create_user, create_channel, create_claim


@mock.patch('src.serializer.User')
@mock.patch('src.serializer.db')
def test_user_serializer(mock_db, mock_user):
  test_user = mock.Mock()
  mock_user.return_value = test_user
  
  result = create_user('mock_user_name')

  assert mock_db.add.called_once()
  assert mock_db.commit.called_once()
  assert result == test_user

@mock.patch('src.serializer.Channel')
@mock.patch('src.serializer.db')
def test_channel_serializer(mock_db, mock_channel):
  test_channel = mock.Mock()
  mock_channel.return_value = test_channel
  
  result = create_channel('mock_channel_id')

  assert mock_db.add.called_once()
  assert mock_db.commit.called_once()
  assert result == test_channel

@mock.patch('src.serializer.Claim')
@mock.patch('src.serializer.db')
def test_claim_serializer(mock_db, mock_claim):
  test_claim = mock.Mock()
  mock_claim.return_value = test_claim

  now = datetime.now()
  result = create_claim(now, 'mock_user_id', 'mock_channel_id')

  assert mock_db.add.called_once()
  assert mock_db.commit.called_once()
  assert result == test_claim
