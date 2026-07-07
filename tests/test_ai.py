from knight_energy.ai import choose_ai_move, difficulty_depth, evaluate_state
from knight_energy.models import (
    BoardItem,
    Difficulty,
    GameState,
    ItemType,
    Player,
    PlayerId,
    Position,
)


def make_state():
    return GameState(
        machine=Player(PlayerId.MACHINE, Position(0, 0), energy=7, score=0),
        human=Player(PlayerId.HUMAN, Position(7, 7), energy=7, score=0),
        items={
            Position(1, 2): BoardItem(ItemType.STAR, 9),
            Position(2, 1): BoardItem(ItemType.STAR, 2),
        },
        turn=PlayerId.MACHINE,
        message="",
    )


def test_difficulty_depths_match_statement():
    assert difficulty_depth(Difficulty.BEGINNER) == 2
    assert difficulty_depth(Difficulty.AMATEUR) == 4
    assert difficulty_depth(Difficulty.EXPERT) == 6


def test_evaluate_state_prefers_machine_advantage():
    better = make_state()
    worse = GameState(
        machine=Player(PlayerId.MACHINE, Position(0, 0), energy=1, score=0),
        human=Player(PlayerId.HUMAN, Position(7, 7), energy=7, score=8),
        items=better.items,
        turn=PlayerId.MACHINE,
        message="",
    )

    assert evaluate_state(better) > evaluate_state(worse)


def test_choose_ai_move_prefers_high_value_reachable_star():
    state = make_state()

    move = choose_ai_move(state, Difficulty.BEGINNER)

    assert move == Position(1, 2)
