from src.game.PlayerState import PlayerState
from src.game.Piece import Piece
from abc import ABC, abstractmethod

class GameState(ABC):

    # BOARD KEY
    # -1 : LOCATION THAT NO PIECE MAY ENTER
    # 0  : EMPTY LOCATION
    # X_Y: X is the player number, Y is the piece type

    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 1
        self.enemy_player = 1
        self.status = None
        self.move_history = []
        self.board_history = []

    @abstractmethod
    def initialize_board(self):
        raise NotImplementedError

    @abstractmethod
    def get_possible_moves(self):
        raise NotImplementedError

    @abstractmethod
    def make_move(self, move, piece):
        raise NotImplementedError

    @abstractmethod
    def undo_move(self):
        raise NotImplementedError

    @abstractmethod
    def is_game_over(self):
        raise NotImplementedError

    @abstractmethod
    def get_winner(self):
        raise NotImplementedError

    # TODO : To be moved to the UI class eventually, here for first iteration
    def display_board(self, board):
        for row in board:
            print(' '.join([str(piece) if piece else '.' for piece in row]))