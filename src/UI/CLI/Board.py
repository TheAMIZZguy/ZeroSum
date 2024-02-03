import src.game.GameState


class DisplayBoard:
    def __init__(self, game, board):
        self.board = board

    def display_board(board):
        for row in board:
            print(' '.join([str(piece) if piece else '.' for piece in row]))