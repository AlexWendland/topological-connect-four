from functools import partial

from topological_connect_four.exceptions import GameException
from topological_connect_four.game_engine.board import NOT_A_POSITION, Board
from topological_connect_four.game_engine.gravity import ValidationFunction
from topological_connect_four.game_engine.models import Player


def longest_line(board: Board, column: int, row: int, column_delta: int, row_delta: int):
    current_player = board.get_position(column, row)
    if current_player == NOT_A_POSITION or current_player == Player.NO_PLAYER:
        raise GameException(f"No player at ({column}, {row}) or not a position")
    line_length = 1
    current_column = column + column_delta
    current_row = row + row_delta
    while line_length < board._size:
        if board.get_position(current_column, current_row) != current_player:
            break
        line_length += 1
        current_column += column_delta
        current_row += row_delta
    current_column = column - column_delta
    current_row = row - row_delta
    while line_length < board._size:
        if board.get_position(current_column, current_row) != current_player:
            break
        line_length += 1
        current_column -= column_delta
        current_row -= row_delta
    return line_length


def has_position_won(board: Board, column: int, row: int, win_length: int = 4):
    return any(
        [
            longest_line(board, column, row, 1, 0) >= win_length,
            longest_line(board, column, row, 0, 1) >= win_length,
            longest_line(board, column, row, 1, 1) >= win_length,
            longest_line(board, column, row, 1, -1) >= win_length,
        ]
    )


class Game:
    def __init__(self, board: Board, gravity: ValidationFunction, number_of_players: int):
        if number_of_players < 2:
            raise ValueError(f"You can not have a game with {number_of_players} you need atleast 2")
        self._number_of_players = number_of_players
        # TODO: Would be good to add a copy function here.
        self._board = board
        self._next_player = Player.ONE
        self._finished = False
        self.valid_move = partial(gravity, self._board)
        self.has_position_won = partial(has_position_won, self._board)

    def _progress_next_player(self):
        # Player numbers are 1 indexed but modulus is 0 indexed.
        next_player_number = self._next_player.value % self._number_of_players
        self._next_player = Player.from_value(next_player_number + 1)

    def make_move(self, player: Player, column: int, row: int):
        if self._finished:
            raise GameException("The game has finished no legal move")
        if player != self._next_player:
            raise GameException(
                f"It is not player {player} go, it is curently player {self._next_player}'s go."
            )
        if not self.valid_move(column, row):
            raise GameException(f"Move ({row}, {column}) is not valid.")
        self._board.set_position_safe(column, row, player)
        if self.has_position_won(column, row):
            self._finished = True
        else:
            self._progress_next_player()

    def __str__(self):
        representation = str(self._board) + "\n --- "
        if self._finished:
            representation += f"Player {self._next_player} has won!\n"
        else:
            representation += f"Next player to move is {self._next_player}.\n"
        representation += " ---"
        return representation
