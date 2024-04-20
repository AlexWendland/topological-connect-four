import enum

import pydantic


class ApiTopology(enum.Enum):
    NONE = "none"
    TORUS = "torus"

class ApiGravity(enum.Enum):
    NONE = "none"
    BOTTOM = "bottom"
    EDGE = "edge"

class Move(pydantic.BaseModel):
    board_id: int
    move_number: int
    player: int
    column: int
    row: int

class GameSettings(pydantic.BaseModel):
    board_size: int
    topology: ApiTopology
    gravity: ApiGravity
    players: int

class GameState(pydantic.BaseModel):
    board: str
    next_player: int
    finished: bool
