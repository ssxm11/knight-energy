from knight_energy.models import (
    BOARD_SIZE,
    ENERGY_VALUES,
    STAR_VALUES,
    BoardItem,
    ItemType,
    Position,
)
from knight_energy.rules import create_random_items, create_random_positions, legal_knight_moves


def test_legal_knight_moves_from_corner():
    moves = set(legal_knight_moves(Position(0, 0)))

    assert moves == {Position(1, 2), Position(2, 1)}


def test_legal_knight_moves_from_center_has_eight_options():
    moves = set(legal_knight_moves(Position(3, 3)))

    assert moves == {
        Position(1, 2),
        Position(1, 4),
        Position(2, 1),
        Position(2, 5),
        Position(4, 1),
        Position(4, 5),
        Position(5, 2),
        Position(5, 4),
    }


def test_random_positions_do_not_overlap():
    positions = create_random_positions(13, seed=7)

    assert len(positions) == 13
    assert len(set(positions)) == 13
    assert all(
        0 <= position.row < BOARD_SIZE and 0 <= position.col < BOARD_SIZE
        for position in positions
    )


def test_random_items_include_expected_star_and_energy_values_without_overlap():
    occupied = {Position(0, 0), Position(7, 7)}

    items = create_random_items(occupied, seed=3)

    assert sorted(item.value for item in items.values() if item.item_type == ItemType.STAR) == STAR_VALUES
    assert sorted(item.value for item in items.values() if item.item_type == ItemType.ENERGY) == ENERGY_VALUES
    assert not occupied.intersection(items)
    assert all(isinstance(item, BoardItem) for item in items.values())
