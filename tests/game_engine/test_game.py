import pytest

from topological_connect_four.exceptions import GameException
from topological_connect_four.game_engine.board import BandBoard, Board
from topological_connect_four.game_engine.game import has_position_won, longest_line
from topological_connect_four.game_engine.models import Player


@pytest.fixture
def band_board():
    """
    4: - - - 1 -
    3: - 1 2 1 -
    2: - 1 - 1 -
    1: 1 1 1 1 1
    0: - - - - 1
       ---------
       0 1 2 3 4
    """
    board = BandBoard(size=5)
    for column, row in [
        (0, 1),
        (1, 1),
        (1, 2),
        (1, 3),
        (2, 1),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4),
        (4, 0),
        (4, 1),
    ]:
        board.set_position(column, row, Player.ONE)
    board.set_position(2, 3, Player.TWO)
    return board


@pytest.mark.parametrize(
    ["column", "row", "column_delta", "row_delta", "expected"],
    [
        (3, 4, 1, 0, 1),
        (4, 0, 0, 1, 2),
        (1, 2, 0, 1, 3),
        (2, 1, 1, 1, 2),
        (2, 1, 1, -1, 2),
        (3, 2, 0, 1, 4),
        (3, 2, 0, -1, 4),
        (3, 2, 1, 0, 1),
        (3, 3, 1, 0, 1),
        (2, 1, 1, 0, 5),
        (0, 1, 1, 1, 3),
    ],
    ids=[
        "Single",
        "Double",
        "Tripple center start",
        "Forward diagonal",
        "Backward diagonal",
        "Four center start",
        "Test negative straight",
        "Gap",
        "Player intercept",
        "Infinite loop",
        "Using geomtry",
    ],
)
def test_longest_line(
    band_board: Board, column: int, row: int, column_delta: int, row_delta: int, expected: int
):
    assert longest_line(band_board, column, row, column_delta, row_delta) == expected


@pytest.mark.parametrize(
    ["column", "row", "column_delta", "row_delta"],
    [
        (0, 4, 1, 0),
        (0, 5, 1, 0),
    ],
    ids=["No player", "Not a positon"],
)
def test_longest_line_fails(
    band_board: BandBoard, column: int, row: int, column_delta: int, row_delta: int
):
    with pytest.raises(GameException):
        longest_line(band_board, column, row, column_delta, row_delta)


@pytest.mark.parametrize(
    ["column", "row", "has_won"], [(3, 2, True), (2, 1, True), (1, 2, False), (4, 0, False)]
)
def test_has_position_won(band_board: BandBoard, column: int, row: int, has_won: bool):
    assert has_position_won(band_board, column, row, win_length=4) == has_won
