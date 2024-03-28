from game.game import Game
from game.board import NoGeometryBoard
from game.gravity import bottom_gravity

if __name__ == "__main__":
    my_game = Game(board=NoGeometryBoard(size=8), gravity=bottom_gravity)
    print(str(my_game))
    while not my_game._finished:
        move = input(
            f"Where should Player {my_game._next_player} play?\n(Put in two numbers column row e.g. 0 2)"
        )
        try:
            column, row = move.split(" ")
            my_game.make_move(my_game._next_player, int(column), int(row))
        except (ValueError, TypeError) as move_error:
            print(move_error)
            print("Try that move again.")
        print(str(my_game))
