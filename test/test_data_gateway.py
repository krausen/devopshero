from datetime import datetime
from unittest import mock
from src.data_gateway import create_user, create_channel, create_claim


@mock.patch('src.data_gateway.User')
@mock.patch('src.data_gateway.db')
def test_create_user(mock_db, mock_user):
    test_user = mock.Mock()
    mock_user.return_value = test_user

    result = create_user('mock_user_name')

    assert mock_db.add.called_once()
    assert mock_db.commit.called_once()
    assert result == test_user


@mock.patch('src.data_gateway.Channel')
@mock.patch('src.data_gateway.db')
def test_create_channel(mock_db, mock_channel):
    test_channel = mock.Mock()
    mock_channel.return_value = test_channel

    result = create_channel('mock_channel_id')

    assert mock_db.add.called_once()
    assert mock_db.commit.called_once()
    assert result == test_channel


@mock.patch('src.data_gateway.Claim')
@mock.patch('src.data_gateway.db')
def test_create_claim(mock_db, mock_claim):
    test_claim = mock.Mock()
    mock_claim.return_value = test_claim

    now = datetime.now()
    result = create_claim(now, 'mock_user_id', 'mock_channel_id')

    assert mock_db.add.called_once()
    assert mock_db.commit.called_once()
    assert result == test_claim
