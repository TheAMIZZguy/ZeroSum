from src.game.GameState import GameState
from src.game.PlayerState import PlayerState
from src.game.Piece import Piece
from copy import deepcopy

from src.games.ReversiMan.game.pieces.Piece1 import Piece1

## ALL OF THIS BELOW WAS BECAUSE I WAS TRYING TO HAVE THE CODE IMPORT EVERYTHING PROGRAMICALLY WITH THE __IMPORT
## BUT LIKE, AFTER THE PIECES ARE DEFINED IT SHOULD ALREADY BE ABLE TO AUTO-CONCACTENATE IT TO THE FILE (see above)
# import os
# # print(os.path.dirname(__file__))
# for module in os.listdir(os.path.dirname(__file__) + r"/pieces"):
#     if module == "__init__.py" or module[-3:] != ".py":
#         continue
#     __import__("src.games.ReversiMan.game.pieces." + module[:-3], locals(), globals())
# del module
# import src.games.ReversiMan.game.pieces


class ReversiManState(GameState):

    def __init__(self):
        super().__init__()

    def initialize_board(self):
        # Rows: 8
        # Columns: 8
        self.board = [[0]*8]*8

        # Player 1 Pieces:
        # Type 1
        self.board[3][3] = Piece1(1)
        self.board[4][4] = Piece1(1)

        # Player 2 Pieces:
        # Selection: Reflect Horizontally
        # Type 1
        self.board[(len(self.board)-1) - 3][len(self.board[(len(self.board)-1) - 3]) - 3] = Piece1(2)
        self.board[(len(self.board)-1) - 4][len(self.board[(len(self.board)-1) - 4]) - 4] = Piece1(2)

        self.move_history.append("")
        self.board_history.append(deepcopy(self.board))


    def get_possible_moves(self):

        # TODO something about piece type

        possible_moves = []
        for x, row in enumerate(self.board):
            for y, piece in enumerate(row):
                # Selected: Empty Tile placement
                if piece != 0:
                    continue

                # Subselection: Adjacent to another
                left, right, up, down = -1, -1, -1, -1
                if y > 0:
                    left = self.board[x][y-1].team
                if y + 1 < len(self.board[x]):
                    right = self.board[x][y+1].team
                if x > 0:
                    up = self.board[x-1][y].team
                if x + 1 < len(self.board):
                    down = self.board[x+1][y].team

                # Subselection: Diagonal to another
                upleft, upright, downleft, downright = -1, -1, -1, -1
                if y > 0 and x > 0:
                    upleft = self.board[x-1][y-1].team
                if y + 1 < len(self.board[x]) and x > 0:
                    upright = self.board[x-1][y+1].team
                if y > 0 and x + 1 < len(self.board):
                    downleft = self.board[x+1][y-1].team
                if y + 1 < len(self.board[x]) and x + 1 < len(self.board):
                    downright = self.board[x+1][y+1].team

                # Restriction: Adjacent to Enemy
                if self.enemy_player not in [left, right, up, down, upleft, upright, downleft, downright]:
                    continue

                # Subrestriction: Form line to self piece
                satisfies_subrestriction = False
                if self.enemy_player == left:
                    i = 0
                    while i <= y:
                        if self.board[x][y-i].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x][y-i].team == 0:
                            break
                        i += 1
                if not satisfies_subrestriction and self.enemy_player == right:
                    i = 0
                    while i < len(self.board[x]) - y:
                        if self.board[x][y+i].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x][y+i].team == 0:
                            break
                        i += 1
                if not satisfies_subrestriction and self.enemy_player == up:
                    i = 0
                    while i < x:
                        if self.board[x-i][y].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x-i][y].team == 0:
                            break
                        i += 1
                if not satisfies_subrestriction and self.enemy_player == down:
                    i = 0
                    while i < len(self.board) - x:
                        if self.board[x+1][y].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x+1][y].team == 0:
                            break
                        i += 1

                # Subrestriction: Form diagonal to self piece
                if self.enemy_player == upleft:
                    i = 0
                    while i <= x and i <= y:  # Not the most efficient, but works for programatic approach
                        if self.board[x-i][y-i].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x-i][y-i].team == 0:
                            break
                        i += 1
                if not satisfies_subrestriction and self.enemy_player == upright:
                    i = 0
                    while i <= x and i < len(self.board[x-i]) - y:
                        if self.board[x-i][y+i].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x-i][y+i].team == 0:
                            break
                        i += 1
                if not satisfies_subrestriction and self.enemy_player == downleft:
                    i = 0
                    while i <= len(self.board) - x and i < y:
                        if self.board[x+i][y-i].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x+i][y-i].team == 0:
                            break
                    i += 1
                if not satisfies_subrestriction and self.enemy_player == downright:
                    i = 0
                    while i < len(self.board) - x and i < len(self.board[x+i]) - y:
                        if self.board[x+i][y+i].team == self.current_player:
                            satisfies_subrestriction = True
                            break
                        if self.board[x+i][y+i].team == 0:
                            break
                        i += 1

                # Done
                if satisfies_subrestriction:
                    possible_moves.append((x,y))

        return possible_moves

    def make_move(self, move, piece):

        x, y = move

        # Game Type is Placement
        self.board[move[0]][move[1]] = piece

        # The board is changed on placement
        # Based on Location
        # Effect is SWAP
        # SWAP effects occur on LINE to OWN
        # LINE allows DIAGONALS, and MOVE THROUGH ENEMY

        # LINE
        left, right, up, down = -1, -1, -1, -1
        if y > 0:
            left = self.board[x][y - 1].team
        if y + 1 < len(self.board[x]):
            right = self.board[x][y + 1].team
        if x > 0:
            up = self.board[x - 1][y].team
        if x + 1 < len(self.board):
            down = self.board[x + 1][y].team

        # LINE ALLOWS DIAGONALS
        upleft, upright, downleft, downright = -1, -1, -1, -1
        if y > 0 and x > 0:
            upleft = self.board[x - 1][y - 1].team
        if y + 1 < len(self.board[x]) and x > 0:
            upright = self.board[x - 1][y + 1].team
        if y > 0 and x + 1 < len(self.board):
            downleft = self.board[x + 1][y - 1].team
        if y + 1 < len(self.board[x]) and x + 1 < len(self.board):
            downright = self.board[x + 1][y + 1].team


        # LINE TO OWN
        if self.enemy_player == left:
            i = 0
            while i <= y:
                # NOT TO OWN
                if self.board[x][y - i].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x][y - i].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x][y - i].team != self.current_player:
                    # SWAP
                    self.board[x][y-i].team = self.current_player
                i += 1
        if self.enemy_player == right:
            i = 0
            while i < len(self.board[x]) - y:
                # NOT TO OWN
                if self.board[x][y + i].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x][y + i].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x][y + i].team != self.current_player:
                    # SWAP
                    self.board[x][y + i].team = self.current_player
                i += 1
        if self.enemy_player == up:
            i = 0
            while i < x:
                # NOT TO OWN
                if self.board[x - i][y].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x - i][y].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x - i][y].team != self.current_player:
                    # SWAP
                    self.board[x - i][y].team = self.current_player
                i += 1
        if self.enemy_player == down:
            i = 0
            while i < len(self.board) - x:
                # NOT TO OWN
                if self.board[x + 1][y].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x + 1][y].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x + 1][y].team != self.current_player:
                    # SWAP
                    self.board[x + 1][y].team = self.current_player
                i += 1

        # ALSO ALOW DIAGONAL
        if self.enemy_player == upleft:
            i = 0
            while i <= x and i <= y:  # Not the most efficient, but works for programatic approach
                # NOT TO OWN
                if self.board[x - i][y - i].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x - i][y - i].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x - i][y - i].team != self.current_player:
                    self.board[x - i][y - i].team = self.current_player
                i += 1
        if self.enemy_player == upright:
            i = 0
            while i <= x and i < len(self.board[x - i]) - y:
                # NOT TO OWN
                if self.board[x - i][y + i].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x - i][y + i].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x - i][y + i].team != self.current_player:
                    self.board[x - i][y + i].team = self.current_player
                i += 1
        if self.enemy_player == downleft:
            i = 0
            while i <= len(self.board) - x and i < y:
                # NOT TO OWN
                if self.board[x + i][y - i].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x + i][y - i].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x + i][y - i].team != self.current_player:
                    self.board[x + i][y - i].team = self.current_player
            i += 1
        if self.enemy_player == downright:
            i = 0
            while i < len(self.board) - x and i < len(self.board[x + i]) - y:
                # NOT TO SELF
                if self.board[x + i][y + i].team == self.current_player:
                    break
                # NOT TO EMPTY
                if self.board[x + i][y + i].team == 0:
                    break
                # LINE on ENEMY
                if self.board[x + i][y + i].team != self.current_player:
                    self.board[x + i][y + i].team = self.current_player
                i += 1


        self.move_history.append(move)
        self.board_history.append(deepcopy(self.board))



    def undo_move(self):
        if not self.move_history:
            return

        self.move_history.pop()
        self.board_history.pop()
        self.board = self.board_history[-1]

    def is_game_over(self):
        # When no moves are possible by any party
        if self.get_possible_moves():
            return False
        self.current_player, self.enemy_player = self.enemy_player, self.current_player
        if self.get_possible_moves():
            self.current_player, self.enemy_player = self.enemy_player, self.current_player
            return False
        self.current_player, self.enemy_player = self.enemy_player, self.current_player
        return True

    def get_winner(self):
        # Winner is one with the most pieces on board
        scores = [0,0]
        for row in self.board:
            for item in row:
                scores[item.team] += 1

        max_score = 0
        max_player = 0
        for player, score in enumerate(scores):
            if score > max_score:
                max_score = score
                max_player = player

        if scores.count(max_score) > 1:
            max_player = 0

        return max_player


    # TODO : To be moved to the UI class eventually, here for first iteration
    def display_board(self, board):
        for row in board:
            print(' '.join([str(piece) if piece else '.' for piece in row]))


