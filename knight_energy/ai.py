from math import inf

from knight_energy.game import apply_move, current_player, game_over, pass_turn
from knight_energy.models import Difficulty, GameState, ItemType, Player, PlayerId, Position
from knight_energy.rules import legal_knight_moves


DEPTH_BY_DIFFICULTY = {
    Difficulty.BEGINNER: 2,
    Difficulty.AMATEUR: 4,
    Difficulty.EXPERT: 6,
}


def difficulty_depth(difficulty: Difficulty) -> int:
    return DEPTH_BY_DIFFICULTY[difficulty]


def choose_ai_move(state: GameState, difficulty: Difficulty) -> Position | None:
    player = current_player(state)
    if player.player_id != PlayerId.MACHINE or player.energy <= 0:
        return None

    best_move = None
    best_value = -inf
    for move in legal_knight_moves(player.position):
        value = _minimax(
            apply_move(state, move),
            difficulty_depth(difficulty) - 1,
            -inf,
            inf,
        )
        if value > best_value or (value == best_value and (best_move is None or move < best_move)):
            best_value = value
            best_move = move
    return best_move


def evaluate_state(state: GameState) -> float:
    score_difference = state.machine.score - state.human.score
    energy_difference = state.machine.energy - state.human.energy
    return (
        10 * score_difference
        + 2 * energy_difference
        + _reachable_item_bonus(state.machine, state)
        - _reachable_item_bonus(state.human, state)
        - _energy_risk_penalty(state.machine)
        + _energy_risk_penalty(state.human)
    )


def _minimax(state: GameState, depth: int, alpha: float, beta: float) -> float:
    if depth == 0 or game_over(state):
        return evaluate_state(state)

    player = current_player(state)
    if player.energy <= 0:
        return _minimax(pass_turn(state), depth - 1, alpha, beta)

    moves = legal_knight_moves(player.position)
    if player.player_id == PlayerId.MACHINE:
        value = -inf
        for move in moves:
            value = max(value, _minimax(apply_move(state, move), depth - 1, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    value = inf
    for move in moves:
        value = min(value, _minimax(apply_move(state, move), depth - 1, alpha, beta))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value


def _reachable_item_bonus(player: Player, state: GameState) -> float:
    if player.energy <= 0:
        return 0

    bonus = 0.0
    one_move_targets = set(legal_knight_moves(player.position))
    for position, item in state.items.items():
        if position in one_move_targets:
            if item.item_type == ItemType.STAR:
                bonus += item.value * 3
            elif item.item_type == ItemType.ENERGY and player.energy <= 3:
                bonus += item.value * 2
    return bonus


def _energy_risk_penalty(player: Player) -> float:
    if player.energy <= 0:
        return 12
    if player.energy == 1:
        return 4
    return 0
