from dataclasses import replace

import pygame

from knight_energy.ai import choose_ai_move
from knight_energy.game import apply_move, can_current_player_move, create_game, game_over, pass_turn
from knight_energy.models import PlayerId
from knight_energy.ui import (
    WINDOW_SIZE,
    board_position_from_pixel,
    create_fonts,
    draw_game,
    draw_game_over,
    draw_menu,
    legal_targets_for_human,
    load_assets,
)


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Knight Energy")
clock = pygame.time.Clock()
running = True
mode = "menu"
game_state = None
menu_buttons = {}
difficulty = None
fonts = create_fonts()
assets = load_assets()

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            mode = "menu"
            game_state = None
            difficulty = None
        elif mode == "menu" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for selected_difficulty, rect in menu_buttons.items():
                if rect.collidepoint(event.pos):
                    game_state = create_game()
                    difficulty = selected_difficulty
                    game_state = replace(
                        game_state,
                        message=f"Dificultad: {difficulty.value}. La maquina inicia.",
                    )
                    mode = "playing"
        elif (
            mode == "playing"
            and game_state
            and game_state.turn == PlayerId.HUMAN
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            target = board_position_from_pixel(event.pos)
            if target in legal_targets_for_human(game_state):
                game_state = apply_move(game_state, target)

    if mode == "menu":
        menu_buttons = draw_menu(screen, fonts, assets, mouse_pos)
    elif game_state:
        if mode == "playing" and game_over(game_state):
            mode = "game_over"
        elif mode == "playing" and not can_current_player_move(game_state):
            game_state = pass_turn(game_state)
        elif mode == "playing" and game_state.turn == PlayerId.MACHINE and difficulty:
            target = choose_ai_move(game_state, difficulty)
            game_state = apply_move(game_state, target) if target else pass_turn(game_state)

        draw_game(
            screen,
            game_state,
            fonts,
            assets,
            selected=game_state.human.position if game_state.turn == PlayerId.HUMAN else None,
            legal_targets=legal_targets_for_human(game_state),
        )
        if mode == "game_over":
            draw_game_over(screen, fonts, game_state)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
