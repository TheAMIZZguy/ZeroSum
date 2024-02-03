from src.game.PlayerState import PlayerState

from src.games.ReversiMan.game.Piece import ReversiManPiece


class Piece1(ReversiManPiece):
    def __init__(self, player: PlayerState):
        super().__init__(player)
        self.piece_type = 1

        # No other selected attributes

    def get_possible_locations(self, current_location):
        # Movement Type: Placement
        raise NotImplementedError

