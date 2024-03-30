from topological_connect_four.exceptions import GameException
from topological_connect_four.game_engine.board import NoGeometryBoard
from topological_connect_four.game_engine.game import Game
from topological_connect_four.game_engine.gravity import bottom_gravity

if __name__ == "__main__":
    my_game = Game(board=NoGeometryBoard(size=8), gravity=bottom_gravity, number_of_players=2)
    print(str(my_game))
    while not my_game._finished:
        moves = my_game.get_avalible_moves()
        prompt = (
            f"Where should Player {my_game._next_player.value} play?\n"
            f"(Put in the key of the move e.g. 0 to play in {moves[0]}.\n"
        )
        for index, move in enumerate(moves):
            prompt += f"  {index:2d}: {str(move)}\n"
        move = input(prompt + "\n > ")
        try:
            column, row = moves[int(move)]
            my_game.make_move(my_game._next_player, int(column), int(row))
        except (ValueError, IndexError, GameException) as move_error:
            print(move_error)
            print("Try that move again.")
        print(str(my_game))
