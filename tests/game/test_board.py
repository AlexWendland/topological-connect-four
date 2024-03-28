from game.board import NoGeometryBoard

import pytest


def test_no_geometry_works():
    board = NoGeometryBoard(size=8)
    assert (0,0) == board._get_coordinates(0,0)
    with pytest.raises(ValueError):
        
