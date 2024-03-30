from topological_connect_four.exceptions import GameException
from topological_connect_four.game_engine.board import NoGeometryBoard
from topological_connect_four.game_engine.game import Game
from topological_connect_four.game_engine.gravity import bottom_gravity

if __name__ == "__main__":
    my_game = Game(board=NoGeometryBoard(size=8), gravity=bottom_gravity, number_of_players=2)
    print(str(my_game))
    while not my_game._finished:
        move = input(
            f"""
            Where should Player {my_game._next_player.value} play?
            (Put in two numbers column row e.g. 0 2)
            """
        )
        try:
            column, row = move.split(" ")
            my_game.make_move(my_game._next_player, int(column), int(row))
        except (ValueError, TypeError, GameException) as move_error:
            print(move_error)
            print("Try that move again.")
        print(str(my_game))
