from src.game.PlayerState import PlayerState
from src.game.Piece import Piece

class ReversiManPiece(Piece):
    def __init__(self, player: PlayerState):
        super().__init__(player)

