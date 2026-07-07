from knight_energy.models import Position
from knight_energy.ui import board_position_from_pixel


def test_board_position_from_pixel_returns_position_inside_board():
    position = board_position_from_pixel((33, 65), board_origin=(32, 64), cell_size=72)

    assert position == Position(0, 0)


def test_board_position_from_pixel_returns_none_outside_board():
    position = board_position_from_pixel((20, 65), board_origin=(32, 64), cell_size=72)

    assert position is None
