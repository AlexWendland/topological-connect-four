from typing import List, Optional, Tuple
from abc import ABC, abstractmethod
from game.models import Player

NOT_A_POSITION = None
AtPosition = Optional[Player]


class Board(ABC):
    def __init__(self, size: int):
        if not (isinstance(size, int) and size > 0):
            raise ValueError(f"Size provided {size} is not a non-zero integer")
        # NOTE: State indicies are row first then column to make printing easier.
        self._state = [[Player.NO_PLAYER] * size for _ in range(size)]
        self._size = size
        # NOTE: This allows for custom drawing of the board.
        self._set_edge_identifier()

    def _set_edge_identifier(self):
        self._edge_identifier = {
            "bottom": "-",
            "top": "-",
            "left": "|",
            "right": "|",
        }

    @abstractmethod
    def _get_coordinates(self, column: int, row: int) -> Optional[Tuple[int, int]]:
        """
        This method is used to implement the geometry of the board. It can apply
        the transformation to the coordinates.

        If the position does not exist on the board return none.
        """

    def get_position(self, column: int, row: int) -> AtPosition:
        coordinates = self._get_coordinates(column, row)
        if coordinates is None:
            return NOT_A_POSITION
        formated_column, formated_row = coordinates
        return self._state[formated_row][formated_column]

    def set_position(self, column: int, row: int, player: Player):
        formated_column, formated_row = self.normalise_coordinates(column, row)
        self._state[formated_row][formated_column] = player

    def set_position_safe(self, column: int, row: int, player: Player):
        formated_column, formated_row = self.normalise_coordinates(column, row)
        if self._state[formated_row][formated_column] != Player.NO_PLAYER:
            other_player = self._state[formated_row][formated_column]
            raise ValueError(
                f"Player {other_player} already in position ({column}, {row}) "
                f"-> ({formated_column},{formated_row})"
            )
        self._state[formated_row][formated_column] = player

    def get_state(self) -> List[List[Player]]:
        return self._state.copy()

    def get_size(self) -> int:
        return self._size

    def normalise_coordinates(self, column: int, row: int) -> Tuple[int, int]:
        """
        This function gets the coordinates of a point in the central grid.
        It raises an error if it isn't a position on the board.
        """
        coordinates = self._get_coordinates(column, row)
        if coordinates is None:
            raise ValueError(f"Position ({column}, {row}) not on the board")
        return coordinates

    def __str__(self) -> str:
        # NOTE: We build the string top to bottom.
        representation = (
            " " * 5 + "." + self._edge_identifier["top"] * (self._size * 2 - 1) + ".\n"
        )

        index = self._size - 1
        for row in reversed(self._state):
            representation += f" {index:2d}: " + self._edge_identifier["left"]
            representation += " ".join(
                [
                    str(player.value) if player != Player.NO_PLAYER else "-"
                    for player in row
                ]
            )
            representation += self._edge_identifier["right"] + "\n"
            index -= 1

        representation += (
            " " * 5
            + "."
            + self._edge_identifier["bottom"] * (self._size * 2 - 1)
            + ".\n"
        )
        representation += " " * 6 + " ".join(
            [str(index) for index in range(self._size)]
        )
        return representation


class NoGeometryBoard(Board):
    def _get_coordinates(self, column: int, row: int) -> Optional[Tuple[int, int]]:
        if (0 <= column < self._size) and (0 <= row < self._size):
            return column, row
        return None


class ToricBoard(Board):
    def _set_edge_identifier(self):
        self._edge_identifier = {
            "bottom": "}",
            "top": "}",
            "left": "^",
            "right": "^",
        }

    def _get_coordinates(self, column: int, row: int) -> Optional[Tuple[int, int]]:
        return column % self._size, row % self._size


class BandBoard(Board):
    def _set_edge_identifier(self):
        self._edge_identifier = {
            "bottom": "-",
            "top": "-",
            "left": "^",
            "right": "^",
        }

    def _get_coordinates(self, column: int, row: int) -> Optional[Tuple[int, int]]:
        if 0 <= row < self._size:
            return column % self._size, row
        return None
