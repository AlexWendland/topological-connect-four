from topological_connect_four.game_engine.board import NoGeometryBoard, NOT_A_POSITION
from topological_connect_four.game_engine.models import Player

import pytest


@pytest.mark.parametrize("size", [1, 4, 11])
def test_initilisation(size: int):
    board = NoGeometryBoard(size=size)
    assert len(board._state) == size
    for row in board._state:
        assert len(row) == size
    assert board._size == size
    assert board._state[0][0] == Player.NO_PLAYER


@pytest.fixture
def no_geometry_board():
    board = NoGeometryBoard(size=5)
    board.set_position(0, 0, Player.ONE)
    board.set_position(0, 1, Player.TWO)
    board.set_position(2, 0, Player.ONE)
    return board


@pytest.mark.parametrize(
    ["column", "row", "player"],
    [
        (0, 0, Player.ONE),
        (0, 1, Player.TWO),
        (2, 2, Player.NO_PLAYER),
        (-1, -1, NOT_A_POSITION),
    ],
)
def test_get_position(no_geometry_board, column, row, player):
    assert no_geometry_board.get_position(column, row) == player
