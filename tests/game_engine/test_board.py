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


# @pytest.fixture
