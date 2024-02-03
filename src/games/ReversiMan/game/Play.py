from src.games.ReversiMan.game.GameState import ReversiManState

# This is direct because it can be auto-imported
from src.games.ReversiMan.game.pieces.Piece1 import Piece1

game = ReversiManState()
while not game.is_game_over():
    game.display_board()

    print("It is Player " + game.current_player + "'s Turn")
    print("Moves are: ")
    possible_moves = game.get_possible_moves()
    print(" ".join(possible_moves))

    while True:
        move = input("Enter move: ")
        move = move[1:-1].split(",")

        if move not in possible_moves:
            continue

        # TODO assign names to piece numbers
        # This can also be done directly
        piece_num = int(input("Enter Piece: (number from 1 to 1)"))
        if 0 >= piece_num or piece_num < 1:
            continue

        game.make_move(move, Piece1())
        break

winner = game.get_winner()

if not winner:
    print("It's a Tie")
else:
    print("Player " + str(winner) + " Wins!")

