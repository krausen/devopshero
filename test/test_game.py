from unittest import mock, TestCase
import datetime

from src.interactors.stop_game import _sort_high_score, _get_high_score


def test_sort_high_score():
    high_score = {'user_a': 3, 'user_b': 4}

    sorted_high_score = _sort_high_score(high_score)

    assert high_score == {'user_b': 4, 'user_a': 3}


@mock.patch('src.data_gateway')
def get_high_score_sorted(mock_gateway):
    user_a = mock.Mock()
    user_b = mock.Mock()
    user_a.user_name = 'a'
    user_b.user_name = 'b'
    user_a.id = 1
    user_b.id = 2
    claim_a = mock.Mock()
    claim_b = mock.Mock()
    claim_c = mock.Mock()
    mock_gateway.get_claims.return_value = [claim_a, claim_b, claim_c]
    mock_gateway.get_user.side_effect = [user_a, user_a, user_b]

    sorted_high_score = _get_high_score('mock_channel_id', True)

    assert False
