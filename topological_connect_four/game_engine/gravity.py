from typing import Callable

from topological_connect_four.game_engine.board import Board
from topological_connect_four.game_engine.models import Player

ValidationFunction = Callable[[Board, int, int], bool]


def no_gravity(board: Board, column: int, row: int) -> bool:
    return board.get_position(column, row) == Player.NO_PLAYER


def check_direction(
    board: Board,
    normalised_column: int,
    normalised_row: int,
    column_delta: int,
    row_delta: int,
) -> bool:
    normalised_column += column_delta
    normalised_row += row_delta
    while (0 <= normalised_column < board._size) and (
        0 <= normalised_row < board._size
    ):
        if board.get_position(normalised_column, normalised_row) == Player.NO_PLAYER:
            return False
        normalised_column += column_delta
        normalised_row += row_delta
    return True


def bottom_gravity(board: Board, column: int, row: int) -> bool:
    if board.get_position(column, row) != Player.NO_PLAYER:
        return False
    column, row = board.normalise_coordinates(column, row)
    return check_direction(board, column, row, 0, -1)


def any_side_gravity(board: Board, column: int, row: int) -> bool:
    if board.get_position(column, row) != Player.NO_PLAYER:
        return False
    column, row = board.normalise_coordinates(column, row)
    return any(
        [
            check_direction(board, column, row, 1, 0),
            check_direction(board, column, row, -1, 0),
            check_direction(board, column, row, 0, 1),
            check_direction(board, column, row, 0, -1),
        ]
    )
