from src.game import _sort_high_score

def test_sort_high_score():
  high_score = {'user_a': 3, 'user_b': 4}

  sorted_high_score = _sort_high_score(high_score)

  assert high_score == {'user_b': 4, 'user_a': 3}