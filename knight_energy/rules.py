import random

from knight_energy.models import (
    BOARD_SIZE,
    ENERGY_VALUES,
    STAR_VALUES,
    BoardItem,
    ItemType,
    Position,
)


KNIGHT_DELTAS = (
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
)


def is_inside_board(position: Position) -> bool:
    return 0 <= position.row < BOARD_SIZE and 0 <= position.col < BOARD_SIZE


def legal_knight_moves(position: Position) -> list[Position]:
    moves = [
        Position(position.row + row_delta, position.col + col_delta)
        for row_delta, col_delta in KNIGHT_DELTAS
    ]
    return sorted(move for move in moves if is_inside_board(move))


def create_random_positions(count: int, seed: int | None = None) -> list[Position]:
    rng = random.Random(seed)
    all_positions = [
        Position(row, col)
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
    ]
    return rng.sample(all_positions, count)


def create_random_items(
    occupied: set[Position],
    seed: int | None = None,
) -> dict[Position, BoardItem]:
    rng = random.Random(seed)
    available = [
        Position(row, col)
        for row in range(BOARD_SIZE)
        for col in range(BOARD_SIZE)
        if Position(row, col) not in occupied
    ]
    selected = rng.sample(available, len(STAR_VALUES) + len(ENERGY_VALUES))

    items = [
        *(BoardItem(ItemType.STAR, value) for value in STAR_VALUES),
        *(BoardItem(ItemType.ENERGY, value) for value in ENERGY_VALUES),
    ]
    rng.shuffle(items)
    return dict(zip(selected, items))
