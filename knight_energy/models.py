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


class PlayerId(Enum):
    MACHINE = "machine"
    HUMAN = "human"


class Difficulty(Enum):
    BEGINNER = "principiante"
    AMATEUR = "amateur"
    EXPERT = "experto"


@dataclass(frozen=True)
class Player:
    player_id: PlayerId
    position: Position
    energy: int
    score: int = 0


@dataclass(frozen=True)
class GameState:
    machine: Player
    human: Player
    items: dict[Position, BoardItem]
    turn: PlayerId
    message: str
