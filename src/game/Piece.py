from src.game.PlayerState import PlayerState


class Piece:
    def __init__(self, player: int):
        self.team = player
        self.piece_type = None

        self.life = None
        self.offense = None
        self.defense = None
        self.other = None

    def __str__(self):
        return f'{self.team}_{self.piece_type}'

    def get_possible_locations(self, current_location):
        raise NotImplementedError

