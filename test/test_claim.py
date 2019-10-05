from datetime import datetime
from unittest import mock

from hero.usecases.claim import try_to_claim
from hero.entities.claim import Claim


@mock.patch("hero.usecases.claim.create_claim")
@mock.patch("hero.usecases.claim.channel_exist")
@mock.patch("hero.usecases.claim.user_exist")
def test_try_to_claim(mock_user_exist, mock_channel_exist, mock_create_claim):
    mock_user_exist.return_value = True
    mock_channel_exist.return_value = True
    mock_claim = Claim(datetime.now(), user=mock.Mock(), channel=mock.Mock())
    mock_create_claim.return_value = mock_claim

    claim = try_to_claim("mock_user_name", "mock_channel_id")

    assert claim == mock_claim


@mock.patch("hero.usecases.claim.create_user")
@mock.patch("hero.usecases.claim.create_channel")
@mock.patch("hero.usecases.claim.create_claim")
@mock.patch("hero.usecases.claim.channel_exist")
@mock.patch("hero.usecases.claim.user_exist")
def test_try_to_claim_no_user_no_channel(
    mock_user_exist,
    mock_channel_exist,
    mock_create_claim,
    mock_create_channel,
    mock_create_user,
):
    mock_user_exist.return_value = False
    mock_channel_exist.return_value = False
    mock_claim = Claim(datetime.now(), user=mock.Mock(), channel=mock.Mock())
    mock_create_claim.return_value = mock_claim

    claim = try_to_claim("mock_user_name", "mock_channel_id")

    assert claim == mock_claim
    mock_create_channel.assert_called_once_with("mock_channel_id")
    mock_create_user.assert_called_once_with("mock_user_name")
