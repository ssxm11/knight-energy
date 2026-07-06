from dataclasses import dataclass
from enum import Enum


BOARD_SIZE = 8
STAR_VALUES = [2, 3, 4, 5, 6, 8, 9]
ENERGY_VALUES = [2, 3, 4, 5]


@dataclass(frozen=True, order=True)
class Position:
    row: int
    col: int


class ItemType(Enum):
    STAR = "star"
    ENERGY = "energy"


@dataclass(frozen=True)
class BoardItem:
    item_type: ItemType
    value: int
