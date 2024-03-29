from game.board import NoGeometryBoard, ToricBoard
from game.models import Player
from game.gravity import no_gravity, check_direction, bottom_gravity, any_side_gravity

if __name__ == "__main__":
    test_board_1 = NoGeometryBoard(size=4)
    # 3: - - - -
    # 2: 2 1 - -
    # 1: 1 - - 1
    # 0: - 1 1 -
    test_board_1.set_position(0, 1, Player.ONE)
    test_board_1.set_position(0, 2, Player.TWO)
    test_board_1.set_position(1, 0, Player.ONE)
    test_board_1.set_position(1, 2, Player.ONE)
    test_board_1.set_position(2, 0, Player.ONE)
    test_board_1.set_position(3, 1, Player.ONE)

    print(str(test_board_1))
    assert no_gravity(test_board_1, 0, 0)
    assert not no_gravity(test_board_1, 1, 0)
    assert check_direction(test_board_1, 1, 1, -1, 0)
    assert check_direction(test_board_1, 1, 1, 0, -1)
    assert not check_direction(test_board_1, 1, 1, 0, 1)
    assert bottom_gravity(test_board_1, 1, 1)
    assert bottom_gravity(test_board_1, 0, 0)
    assert not bottom_gravity(test_board_1, 1, 3)
    assert any_side_gravity(test_board_1, 1, 1)
    assert any_side_gravity(test_board_1, 2, 2)
    assert not any_side_gravity(test_board_1, 1, 2)

    test_board_2 = ToricBoard(size=4)
    print(str(test_board_2))
    assert not any_side_gravity(test_board_2, 1, 1)
