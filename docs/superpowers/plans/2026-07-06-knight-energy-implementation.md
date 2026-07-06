# Knight Energy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete Pygame implementation of Knight Energy with tested game rules, minimax AI, visual assets, difficulty selection, gameplay loop, and heuristic report.

**Architecture:** Keep domain logic independent from Pygame so tests can exercise rules, state transitions, and minimax without opening a window. `main.py` owns application startup, while `knight_energy/` contains models, rules, game transitions, AI, and UI helpers.

**Tech Stack:** Python 3, Pygame, pytest, dataclasses, standard-library `random`, `math`, and `copy`.

---

## File Structure

- Create `knight_energy/__init__.py`: package marker.
- Create `knight_energy/models.py`: immutable positions, item/player/game dataclasses, difficulty constants.
- Create `knight_energy/rules.py`: board bounds, knight move generation, random setup helpers.
- Create `knight_energy/game.py`: game creation, movement application, turn progression, pass penalties, winner detection.
- Create `knight_energy/ai.py`: minimax, heuristic scoring, AI move selection.
- Create `knight_energy/ui.py`: asset loading, menu drawing, board drawing, status panels, click-to-board conversion.
- Modify `main.py`: run Pygame app using the domain and UI modules.
- Create `tests/test_rules.py`: rule and setup tests.
- Create `tests/test_game.py`: state transition and end-condition tests.
- Create `tests/test_ai.py`: minimax and heuristic tests.
- Create `requirements.txt`: dependencies for pygame and pytest.
- Create `informe.md`: explanation of heuristic utility function.

---

### Task 1: Domain Models And Rules

**Files:**
- Create: `knight_energy/__init__.py`
- Create: `knight_energy/models.py`
- Create: `knight_energy/rules.py`
- Create: `tests/test_rules.py`
- Create: `requirements.txt`

- [ ] **Step 1: Write failing tests for movement and setup**

```python
# tests/test_rules.py
from knight_energy.models import BOARD_SIZE, ENERGY_VALUES, STAR_VALUES, BoardItem, ItemType, Position
from knight_energy.rules import create_random_items, create_random_positions, legal_knight_moves


def test_legal_knight_moves_from_corner():
    moves = set(legal_knight_moves(Position(0, 0)))

    assert moves == {Position(1, 2), Position(2, 1)}


def test_legal_knight_moves_from_center_has_eight_options():
    moves = set(legal_knight_moves(Position(3, 3)))

    assert moves == {
        Position(1, 2), Position(1, 4), Position(2, 1), Position(2, 5),
        Position(4, 1), Position(4, 5), Position(5, 2), Position(5, 4),
    }


def test_random_positions_do_not_overlap():
    positions = create_random_positions(13, seed=7)

    assert len(positions) == 13
    assert len(set(positions)) == 13
    assert all(0 <= position.row < BOARD_SIZE and 0 <= position.col < BOARD_SIZE for position in positions)


def test_random_items_include_expected_star_and_energy_values_without_overlap():
    occupied = {Position(0, 0), Position(7, 7)}

    items = create_random_items(occupied, seed=3)

    assert sorted(item.value for item in items.values() if item.item_type == ItemType.STAR) == STAR_VALUES
    assert sorted(item.value for item in items.values() if item.item_type == ItemType.ENERGY) == ENERGY_VALUES
    assert not occupied.intersection(items)
    assert all(isinstance(item, BoardItem) for item in items.values())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_rules.py -v`
Expected: fail during import because `knight_energy.models` and `knight_energy.rules` do not exist.

- [ ] **Step 3: Implement minimal models and rules**

Create the package, constants, dataclasses, legal move generation, and seeded random setup.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_rules.py -v`
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt knight_energy/__init__.py knight_energy/models.py knight_energy/rules.py tests/test_rules.py
git commit -m "feat: add game domain and rules"
```

---

### Task 2: Game State Transitions

**Files:**
- Modify: `knight_energy/models.py`
- Create: `knight_energy/game.py`
- Create: `tests/test_game.py`

- [ ] **Step 1: Write failing tests for movement, item consumption, pass penalties, and winner detection**

```python
# tests/test_game.py
from knight_energy.game import apply_move, create_game, current_player, game_over, pass_turn, winner
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


def test_winner_returns_none_for_tie():
    state = state_with()

    assert winner(state) is None


def test_create_game_places_all_entities_without_overlap():
    state = create_game(seed=11)
    positions = [state.machine.position, state.human.position, *state.items.keys()]

    assert len(positions) == 13
    assert len(set(positions)) == 13
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_game.py -v`
Expected: fail during import because `knight_energy.game` does not exist.

- [ ] **Step 3: Implement state transitions**

Create `create_game`, `apply_move`, `pass_turn`, `current_player`, `game_over`, and `winner`. Keep transitions immutable by returning copied dataclass instances.

- [ ] **Step 4: Run rule and game tests**

Run: `pytest tests/test_rules.py tests/test_game.py -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add knight_energy/models.py knight_energy/game.py tests/test_game.py
git commit -m "feat: add game state transitions"
```

---

### Task 3: Minimax AI

**Files:**
- Create: `knight_energy/ai.py`
- Create: `tests/test_ai.py`

- [ ] **Step 1: Write failing AI tests**

```python
# tests/test_ai.py
from knight_energy.ai import choose_ai_move, difficulty_depth, evaluate_state
from knight_energy.models import BoardItem, Difficulty, GameState, ItemType, Player, PlayerId, Position


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_ai.py -v`
Expected: fail during import because `knight_energy.ai` does not exist.

- [ ] **Step 3: Implement heuristic and minimax**

Implement difficulty depths, legal successor generation, pass handling for zero-energy players, alpha-beta pruning, and deterministic tie-breaking by utility then row/column order.

- [ ] **Step 4: Run all non-UI tests**

Run: `pytest tests/test_rules.py tests/test_game.py tests/test_ai.py -v`
Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add knight_energy/ai.py tests/test_ai.py
git commit -m "feat: add minimax ai"
```

---

### Task 4: Pygame UI And Assets

**Files:**
- Create: `knight_energy/ui.py`
- Modify: `main.py`

- [ ] **Step 1: Add visual layer using existing assets**

Load `assets/white-horse.png`, `assets/black-horse.png`, `assets/star.png`, `assets/lighting.png`, and optionally `assets/logo.png`. Render an 8 x 8 board, item icons with numeric labels beside them, horses, status panel, difficulty menu, and game-over result.

- [ ] **Step 2: Run syntax check**

Run: `python -m compileall main.py knight_energy`
Expected: exit code 0.

- [ ] **Step 3: Manually launch UI**

Run: `python main.py`
Expected: Pygame window opens, difficulty can be selected, board appears with assets and values, and the human can click legal moves.

- [ ] **Step 4: Commit**

```bash
git add main.py knight_energy/ui.py assets tablero-ejemplo.png enunciado.md
git commit -m "feat: add pygame board ui"
```

---

### Task 5: Integrated Gameplay Loop

**Files:**
- Modify: `main.py`
- Modify: `knight_energy/ui.py`
- Modify: `knight_energy/game.py`

- [ ] **Step 1: Connect AI and human turns**

Machine turns call `choose_ai_move`; human turns accept only legal clicked moves. If a player has no energy, call `pass_turn`. Stop when `game_over` is true and display `winner`.

- [ ] **Step 2: Run automated checks**

Run: `pytest -v`
Expected: all tests pass.

Run: `python -m compileall main.py knight_energy`
Expected: exit code 0.

- [ ] **Step 3: Manual smoke test**

Run: `python main.py`
Expected: complete at least a few turns at beginner difficulty, confirming score/energy changes and item consumption.

- [ ] **Step 4: Commit**

```bash
git add main.py knight_energy/ui.py knight_energy/game.py
git commit -m "feat: integrate gameplay loop"
```

---

### Task 6: Heuristic Report And Final Verification

**Files:**
- Create: `informe.md`
- Modify: `README.md`

- [ ] **Step 1: Write report**

Explain the minimax utility function:

```text
utility = 10 * score_difference
        + 2 * energy_difference
        + reachable_star_bonus
        + low_energy_recovery_bonus
        - mobility_risk_penalty
```

Describe why points dominate the heuristic, why energy matters as future mobility, why reachable high-value objects matter, and why no-energy states are penalized.

- [ ] **Step 2: Update README**

Document install/run/test commands:

```bash
pip install -r requirements.txt
python main.py
pytest -v
```

- [ ] **Step 3: Run final verification**

Run: `pytest -v`
Expected: all tests pass.

Run: `python -m compileall main.py knight_energy`
Expected: exit code 0.

- [ ] **Step 4: Commit**

```bash
git add README.md informe.md
git commit -m "docs: add heuristic report"
```

