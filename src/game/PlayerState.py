

class PlayerState:
    def __init__(self):
        self.team = None
        self.status = None

    def get_team(self):
        raise NotImplementedError

