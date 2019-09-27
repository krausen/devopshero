from datetime import datetime
from unittest import mock

from src.usecases.claim import try_to_claim
from src.entities.claim import Claim


@mock.patch('src.usecases.claim.create_claim')
@mock.patch('src.usecases.claim.channel_exist')
@mock.patch('src.usecases.claim.user_exist')
def test_try_to_claim(mock_user_exist, mock_channel_exist, mock_create_claim):
    mock_user_exist.return_value = True
    mock_channel_exist.return_value = True
    mock_claim = Claim(datetime.now(), user=mock.Mock(), channel=mock.Mock())
    mock_create_claim.return_value = mock_claim

    claim = try_to_claim('mock_user_name', 'mock_channel_id')

    assert claim == mock_claim
