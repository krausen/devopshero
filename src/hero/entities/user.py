class User:
    def __init__(self, user_name):
        self.user_name = user_name

    def __eq__(self, other):
        return self.user_name == other.user_name

    def __hash__(self):
        return hash(self.user_name)

    def __repr__(self):
        return self.user_name
