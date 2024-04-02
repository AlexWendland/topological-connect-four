import pytest

from topological_connect_four.exceptions import GameException
from topological_connect_four.game_engine.board import BandBoard, Board, NoGeometryBoard
from topological_connect_four.game_engine.game import Game, has_position_won, longest_line
from topological_connect_four.game_engine.gravity import no_gravity
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


@pytest.fixture
def simple_game():
    return Game(board=NoGeometryBoard(size=4), gravity=no_gravity, number_of_players=4)


def test_progress_next_player(simple_game):
    assert simple_game._next_player == Player.ONE
    simple_game._progress_next_player()
    assert simple_game._next_player == Player.TWO
    simple_game._progress_next_player()
    assert simple_game._next_player == Player.THREE
    simple_game._progress_next_player()
    assert simple_game._next_player == Player.FOUR
    simple_game._progress_next_player()
    assert simple_game._next_player == Player.ONE


def test_make_move_requires_correct_player(simple_game: Game):
    with pytest.raises(GameException):
        simple_game.make_move(Player.TWO, 0, 0)


def test_game_play(simple_game):
    positions = {}
    board_size = simple_game._board._size
    for column in range(3):
        for row in range(4):
            player = Player.from_value(row + 1)
            simple_game.make_move(player, column, row)
            positions[(column, row)] = player
            for check_column in range(board_size):
                for check_row in range(board_size):
                    assert simple_game._board.get_position(
                        check_column, check_row
                    ) == positions.get((check_column, check_row), Player.NO_PLAYER)
            assert not simple_game._finished
    simple_game.make_move(Player.ONE, 3, 0)
    assert simple_game._finished
