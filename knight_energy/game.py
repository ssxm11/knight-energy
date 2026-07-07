from dataclasses import replace

from knight_energy.models import (
    BoardItem,
    GameState,
    ItemType,
    Player,
    PlayerId,
    Position,
)
from knight_energy.rules import create_random_items, create_random_positions, legal_knight_moves


def create_game(seed: int | None = None) -> GameState:
    machine_position, human_position = create_random_positions(2, seed=seed)
    items = create_random_items(
        {machine_position, human_position},
        seed=None if seed is None else seed + 1,
    )
    return GameState(
        machine=Player(PlayerId.MACHINE, machine_position, energy=7),
        human=Player(PlayerId.HUMAN, human_position, energy=7),
        items=items,
        turn=PlayerId.MACHINE,
        message="La maquina inicia.",
    )


def current_player(state: GameState) -> Player:
    return state.machine if state.turn == PlayerId.MACHINE else state.human


def other_player_id(player_id: PlayerId) -> PlayerId:
    return PlayerId.HUMAN if player_id == PlayerId.MACHINE else PlayerId.MACHINE


def player_has_energy(player: Player) -> bool:
    return player.energy > 0


def can_current_player_move(state: GameState) -> bool:
    return player_has_energy(current_player(state))


def apply_move(state: GameState, target: Position) -> GameState:
    player = current_player(state)
    if not player_has_energy(player):
        raise ValueError("El jugador no tiene energia para moverse.")
    if target not in legal_knight_moves(player.position):
        raise ValueError("El movimiento no es valido para un caballo.")

    items = dict(state.items)
    item = items.pop(target, None)
    energy = player.energy - 1
    score = player.score

    if item and item.item_type == ItemType.STAR:
        score += item.value
    elif item and item.item_type == ItemType.ENERGY:
        energy += item.value

    moved_player = replace(player, position=target, energy=energy, score=score)
    return _state_with_player(
        state,
        moved_player,
        items,
        other_player_id(state.turn),
        _move_message(player.player_id, item),
    )


def pass_turn(state: GameState) -> GameState:
    player = current_player(state)
    penalized = replace(player, score=player.score - 3)
    return _state_with_player(
        state,
        penalized,
        dict(state.items),
        other_player_id(state.turn),
        f"{_player_name(player.player_id)} pierde el turno por falta de energia.",
    )


def game_over(state: GameState) -> bool:
    has_stars = any(item.item_type == ItemType.STAR for item in state.items.values())
    both_without_energy = state.machine.energy <= 0 and state.human.energy <= 0
    return not has_stars or both_without_energy


def winner(state: GameState) -> PlayerId | None:
    if state.machine.score > state.human.score:
        return PlayerId.MACHINE
    if state.human.score > state.machine.score:
        return PlayerId.HUMAN
    return None


def _state_with_player(
    state: GameState,
    player: Player,
    items: dict[Position, BoardItem],
    turn: PlayerId,
    message: str,
) -> GameState:
    if player.player_id == PlayerId.MACHINE:
        return replace(state, machine=player, items=items, turn=turn, message=message)
    return replace(state, human=player, items=items, turn=turn, message=message)


def _move_message(player_id: PlayerId, item: BoardItem | None) -> str:
    name = _player_name(player_id)
    if item and item.item_type == ItemType.STAR:
        return f"{name} recoge {item.value} puntos."
    if item and item.item_type == ItemType.ENERGY:
        return f"{name} recupera {item.value} energia."
    return f"{name} se mueve."


def _player_name(player_id: PlayerId) -> str:
    return "La maquina" if player_id == PlayerId.MACHINE else "El jugador"
