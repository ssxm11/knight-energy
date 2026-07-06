from pathlib import Path

import pygame

from knight_energy.game import winner
from knight_energy.models import BOARD_SIZE, Difficulty, GameState, ItemType, PlayerId, Position
from knight_energy.rules import legal_knight_moves


WINDOW_SIZE = (1040, 720)
BOARD_ORIGIN = (32, 88)
CELL_SIZE = 72
BOARD_PIXEL_SIZE = BOARD_SIZE * CELL_SIZE
PANEL_X = 650
ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"

BACKGROUND = (236, 232, 224)
BOARD_LIGHT = (246, 245, 240)
BOARD_DARK = (216, 214, 205)
GRID = (52, 55, 58)
INK = (37, 39, 42)
MUTED = (94, 98, 104)
ACCENT = (214, 79, 48)
GOOD = (48, 125, 93)
SELECTED = (79, 121, 190)
HIGHLIGHT = (235, 190, 72)
PANEL = (250, 249, 245)


def load_assets() -> dict[str, pygame.Surface]:
    return {
        "white_horse": _load_image("white-horse.png", (58, 58)),
        "black_horse": _load_image("black-horse.png", (58, 58)),
        "star": _load_image("star.png", (32, 32)),
        "energy": _load_image("lighting.png", (30, 30)),
        "logo": _load_image("logo.png", (140, 80)),
    }


def create_fonts() -> dict[str, pygame.font.Font]:
    return {
        "title": pygame.font.SysFont("georgia", 46, bold=True),
        "heading": pygame.font.SysFont("segoeui", 28, bold=True),
        "body": pygame.font.SysFont("segoeui", 22),
        "small": pygame.font.SysFont("segoeui", 18),
        "value": pygame.font.SysFont("segoeui", 22, bold=True),
    }


def board_position_from_pixel(
    point: tuple[int, int],
    board_origin: tuple[int, int] = BOARD_ORIGIN,
    cell_size: int = CELL_SIZE,
) -> Position | None:
    x, y = point
    origin_x, origin_y = board_origin
    col = (x - origin_x) // cell_size
    row = (y - origin_y) // cell_size
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return Position(row, col)
    return None


def draw_menu(
    screen: pygame.Surface,
    fonts: dict[str, pygame.font.Font],
    assets: dict[str, pygame.Surface],
    mouse_pos: tuple[int, int],
) -> dict[Difficulty, pygame.Rect]:
    screen.fill(BACKGROUND)
    logo = assets.get("logo")
    if logo:
        screen.blit(logo, (48, 34))

    _draw_text(screen, "Knight Energy", fonts["title"], INK, (48, 145))
    _draw_text(screen, "Selecciona la dificultad", fonts["heading"], MUTED, (52, 212))

    buttons = {}
    labels = [
        (Difficulty.BEGINNER, "Principiante", "Profundidad 2"),
        (Difficulty.AMATEUR, "Amateur", "Profundidad 4"),
        (Difficulty.EXPERT, "Experto", "Profundidad 6"),
    ]
    for index, (difficulty, label, detail) in enumerate(labels):
        rect = pygame.Rect(56, 285 + index * 82, 360, 58)
        buttons[difficulty] = rect
        is_hover = rect.collidepoint(mouse_pos)
        _draw_button(screen, rect, label, detail, fonts, is_hover)

    preview_rect = pygame.Rect(520, 74, 430, 430)
    pygame.draw.rect(screen, PANEL, preview_rect, border_radius=8)
    pygame.draw.rect(screen, GRID, preview_rect, 2, border_radius=8)
    _draw_text(screen, "La maquina juega primero", fonts["heading"], INK, (548, 116))
    _draw_text(screen, "Caballo blanco: IA", fonts["body"], MUTED, (552, 176))
    _draw_text(screen, "Caballo negro: jugador", fonts["body"], MUTED, (552, 215))
    _draw_text(screen, "Cada movimiento cuesta 1 energia.", fonts["small"], MUTED, (552, 282))
    _draw_text(screen, "Las estrellas y energia se consumen.", fonts["small"], MUTED, (552, 315))
    return buttons


def draw_game(
    screen: pygame.Surface,
    state: GameState,
    fonts: dict[str, pygame.font.Font],
    assets: dict[str, pygame.Surface],
    selected: Position | None = None,
    legal_targets: set[Position] | None = None,
) -> None:
    screen.fill(BACKGROUND)
    _draw_board(screen, fonts, assets, state, selected, legal_targets or set())
    _draw_panel(screen, fonts, state)


def draw_game_over(screen: pygame.Surface, fonts: dict[str, pygame.font.Font], state: GameState) -> None:
    overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)
    overlay.fill((30, 30, 30, 125))
    screen.blit(overlay, (0, 0))
    rect = pygame.Rect(300, 210, 440, 240)
    pygame.draw.rect(screen, PANEL, rect, border_radius=8)
    pygame.draw.rect(screen, GRID, rect, 2, border_radius=8)

    result = winner(state)
    if result == PlayerId.MACHINE:
        title = "Gana la maquina"
    elif result == PlayerId.HUMAN:
        title = "Gana el jugador"
    else:
        title = "Empate"

    _draw_text(screen, "Fin del juego", fonts["heading"], INK, (rect.x + 36, rect.y + 34))
    _draw_text(screen, title, fonts["title"], ACCENT, (rect.x + 36, rect.y + 84))
    _draw_text(screen, "Presiona R para jugar otra vez", fonts["body"], MUTED, (rect.x + 38, rect.y + 170))


def legal_targets_for_human(state: GameState) -> set[Position]:
    if state.turn != PlayerId.HUMAN or state.human.energy <= 0:
        return set()
    return set(legal_knight_moves(state.human.position))


def _draw_board(
    screen: pygame.Surface,
    fonts: dict[str, pygame.font.Font],
    assets: dict[str, pygame.Surface],
    state: GameState,
    selected: Position | None,
    legal_targets: set[Position],
) -> None:
    board_rect = pygame.Rect(*BOARD_ORIGIN, BOARD_PIXEL_SIZE, BOARD_PIXEL_SIZE)
    pygame.draw.rect(screen, GRID, board_rect, 2)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            rect = _cell_rect(Position(row, col))
            color = BOARD_LIGHT if (row + col) % 2 == 0 else BOARD_DARK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID, rect, 1)

    for target in legal_targets:
        pygame.draw.circle(screen, HIGHLIGHT, _cell_center(target), 8)

    if selected:
        pygame.draw.rect(screen, SELECTED, _cell_rect(selected), 3)

    for position, item in state.items.items():
        _draw_item(screen, fonts, assets, position, item.item_type, item.value)

    _draw_horse(screen, assets["white_horse"], state.machine.position)
    _draw_horse(screen, assets["black_horse"], state.human.position)


def _draw_panel(screen: pygame.Surface, fonts: dict[str, pygame.font.Font], state: GameState) -> None:
    panel_rect = pygame.Rect(PANEL_X, 88, 340, 576)
    pygame.draw.rect(screen, PANEL, panel_rect, border_radius=8)
    pygame.draw.rect(screen, GRID, panel_rect, 2, border_radius=8)

    _draw_text(screen, "Estado", fonts["heading"], INK, (PANEL_X + 28, 120))
    turn_text = "Turno: maquina" if state.turn == PlayerId.MACHINE else "Turno: jugador"
    _draw_text(screen, turn_text, fonts["body"], ACCENT, (PANEL_X + 28, 168))

    _draw_text(screen, "Maquina", fonts["heading"], INK, (PANEL_X + 28, 230))
    _draw_text(screen, f"Puntos: {state.machine.score}", fonts["body"], MUTED, (PANEL_X + 32, 272))
    _draw_text(screen, f"Energia: {state.machine.energy}", fonts["body"], MUTED, (PANEL_X + 32, 305))

    _draw_text(screen, "Jugador", fonts["heading"], INK, (PANEL_X + 28, 370))
    _draw_text(screen, f"Puntos: {state.human.score}", fonts["body"], MUTED, (PANEL_X + 32, 412))
    _draw_text(screen, f"Energia: {state.human.energy}", fonts["body"], MUTED, (PANEL_X + 32, 445))

    _draw_wrapped_text(screen, state.message, fonts["small"], MUTED, pygame.Rect(PANEL_X + 28, 525, 284, 92))


def _draw_item(
    screen: pygame.Surface,
    fonts: dict[str, pygame.font.Font],
    assets: dict[str, pygame.Surface],
    position: Position,
    item_type: ItemType,
    value: int,
) -> None:
    rect = _cell_rect(position)
    asset = assets["star"] if item_type == ItemType.STAR else assets["energy"]
    screen.blit(asset, (rect.x + 10, rect.y + 18))
    _draw_text(screen, str(value), fonts["value"], INK, (rect.x + 45, rect.y + 22))


def _draw_horse(screen: pygame.Surface, image: pygame.Surface, position: Position) -> None:
    rect = _cell_rect(position)
    screen.blit(image, (rect.centerx - image.get_width() // 2, rect.centery - image.get_height() // 2))


def _cell_rect(position: Position) -> pygame.Rect:
    return pygame.Rect(
        BOARD_ORIGIN[0] + position.col * CELL_SIZE,
        BOARD_ORIGIN[1] + position.row * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE,
    )


def _cell_center(position: Position) -> tuple[int, int]:
    rect = _cell_rect(position)
    return rect.center


def _draw_button(
    screen: pygame.Surface,
    rect: pygame.Rect,
    label: str,
    detail: str,
    fonts: dict[str, pygame.font.Font],
    is_hover: bool,
) -> None:
    fill = (255, 255, 255) if is_hover else PANEL
    pygame.draw.rect(screen, fill, rect, border_radius=8)
    pygame.draw.rect(screen, ACCENT if is_hover else GRID, rect, 2, border_radius=8)
    _draw_text(screen, label, fonts["body"], INK, (rect.x + 18, rect.y + 9))
    _draw_text(screen, detail, fonts["small"], MUTED, (rect.x + 20, rect.y + 34))


def _draw_text(
    screen: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    pos: tuple[int, int],
) -> None:
    screen.blit(font.render(text, True, color), pos)


def _draw_wrapped_text(
    screen: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    rect: pygame.Rect,
) -> None:
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if font.size(candidate)[0] <= rect.width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    y = rect.y
    for line in lines[:4]:
        _draw_text(screen, line, font, color, (rect.x, y))
        y += font.get_linesize()


def _load_image(filename: str, size: tuple[int, int]) -> pygame.Surface:
    path = ASSET_DIR / filename
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(image, size)
