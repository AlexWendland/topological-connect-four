from pydantic import BaseModel
from enum import Enum


class GravitySetting(Enum):
    NONE = 1
    BOTTOM = 2
    EDGE = 3


class Topology(Enum):
    NONE = 1
    TORUS = 2


# TODO: Make this less hard coded
class Player(Enum):
    NO_PLAYER = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4


class GameState(BaseModel):
    # TODO: Add validation for board size
    board_size: int = 8
    topology: Topology
    gravity: GravitySetting
