from knight_energy.game import apply_move, create_game, game_over, pass_turn, winner
from knight_energy.models import BoardItem, GameState, ItemType, Player, PlayerId, Position


def state_with(item=None, machine_energy=7, human_energy=7):
    items = {}
    if item:
        items[item[0]] = item[1]
    return GameState(
        machine=Player(PlayerId.MACHINE, Position(0, 0), energy=machine_energy),
        human=Player(PlayerId.HUMAN, Position(7, 7), energy=human_energy),
        items=items,
        turn=PlayerId.MACHINE,
        message="",
    )


def test_apply_move_costs_energy_and_collects_star():
    state = state_with((Position(1, 2), BoardItem(ItemType.STAR, 5)))

    new_state = apply_move(state, Position(1, 2))

    assert new_state.machine.position == Position(1, 2)
    assert new_state.machine.energy == 6
    assert new_state.machine.score == 5
    assert Position(1, 2) not in new_state.items
    assert new_state.turn == PlayerId.HUMAN


def test_apply_move_collects_energy_after_paying_move_cost():
    state = state_with((Position(1, 2), BoardItem(ItemType.ENERGY, 4)))

    new_state = apply_move(state, Position(1, 2))

    assert new_state.machine.energy == 10
    assert new_state.machine.score == 0
    assert Position(1, 2) not in new_state.items


def test_pass_turn_penalizes_score_and_changes_turn():
    state = state_with(machine_energy=0)

    new_state = pass_turn(state)

    assert new_state.machine.score == -3
    assert new_state.turn == PlayerId.HUMAN


def test_game_over_when_no_stars_remain():
    state = state_with((Position(1, 2), BoardItem(ItemType.ENERGY, 4)))

    assert game_over(state)


def test_game_over_when_both_players_have_no_energy():
    state = state_with(machine_energy=0, human_energy=0)

    assert game_over(state)


def test_winner_returns_none_for_tie():
    state = state_with()

    assert winner(state) is None


def test_create_game_places_all_entities_without_overlap():
    state = create_game(seed=11)
    positions = [state.machine.position, state.human.position, *state.items.keys()]

    assert len(positions) == 13
    assert len(set(positions)) == 13
