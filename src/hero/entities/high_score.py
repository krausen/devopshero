from hero.entities.user import User


class HighScore:
    def __init__(self):
        self.score_board = {}

    def __len__(self):
        return len(self.score_board)

    def __repr__(self):
        return str(self.score_board)

    def add(self, user):
        if user in self.score_board.keys():
            self.score_board[user] = self.score_board[user] + 1
        else:
            self.score_board[user] = 1

    def sort(self):
        winner_to_loser = sorted(
            self.score_board.keys(),
            key=lambda user: self.score_board[user],
            reverse=True,
        )
        sorted_high_score = {}
        for user in winner_to_loser:
            sorted_high_score[user] = self.score_board[user]
        self.score_board = sorted_high_score

    def get_winners(self):
        highest_score = 0
        best_users = []

        for user, score in self.score_board.items():
            if score > highest_score:
                highest_score = score
                best_users = [user]
            elif score == highest_score:
                best_users.append(user)
        return best_users, highest_score
