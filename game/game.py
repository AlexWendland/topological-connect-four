from game.board import Board, NOT_A_POSITION
from game.models import Player
from game.gravity import ValidationFunction
from functools import partial


def longest_line(
    board: Board, column: int, row: int, column_delta: int, row_delta: int
):
    current_player = board.get_position(column, row)
    if current_player == NOT_A_POSITION or current_player == Player.NO_PLAYER:
        raise ValueError(f"No player at ({column}, {row}) or not a position")
    line_length = 1
    current_column = column + column_delta
    current_row = row + column_delta
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
    # BUG: Seems to be finishing early.
    return any(
        [
            longest_line(board, column, row, 1, 0) >= win_length,
            longest_line(board, column, row, 0, 1) >= win_length,
            longest_line(board, column, row, 1, 1) >= win_length,
            longest_line(board, column, row, 1, -1) >= win_length,
        ]
    )


class Game:
    def __init__(self, board: Board, gravity: ValidationFunction):
        # TODO: Would be good to add a copy function here.
        self._board = board
        self._next_player = Player.ONE
        self._finished = False
        self.valid_move = partial(gravity, self._board)
        self.has_position_won = partial(has_position_won, self._board)

    def _progress_next_player(self):
        # TODO: Make this far less manual.
        if self._next_player == Player.ONE:
            self._next_player = Player.TWO
        elif self._next_player == Player.TWO:
            self._next_player = Player.THREE
        elif self._next_player == Player.THREE:
            self._next_player = Player.FOUR
        elif self._next_player == Player.FOUR:
            self._next_player = Player.ONE

    def make_move(self, player: Player, column: int, row: int):
        if self._finished:
            raise ValueError("The game has finished no legal move")
        if player != self._next_player:
            raise ValueError(
                f"It is not player {player} go, it is curently player {self._next_player}'s go."
            )
        if not self.valid_move(column, row):
            raise ValueError(f"Move ({row}, {column}) is not valid.")
        self._board.set_position_safe(column, row, player)
        if self.has_position_won(column, row):
            self._finished = True
            print(f"Congratulations player {player} has won! The game is now over.")
            return
        self._progress_next_player()

    def __str__(self):
        representation = str(self._board) + "\n --- "
        if self._finished:
            representation += f"Player {self._next_player} has won!\n"
        else:
            representation += f"Next player to move is {self._next_player}.\n"
        representation += " ---"
        return representation
