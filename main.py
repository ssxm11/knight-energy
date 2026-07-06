import pygame

from knight_energy.game import create_game
from knight_energy.ui import WINDOW_SIZE, create_fonts, draw_game, draw_menu, load_assets


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Knight Energy")
clock = pygame.time.Clock()
running = True
mode = "menu"
game_state = None
menu_buttons = {}
fonts = create_fonts()
assets = load_assets()

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif mode == "menu" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for difficulty, rect in menu_buttons.items():
                if rect.collidepoint(event.pos):
                    game_state = create_game()
                    game_state = type(game_state)(
                        machine=game_state.machine,
                        human=game_state.human,
                        items=game_state.items,
                        turn=game_state.turn,
                        message=f"Dificultad: {difficulty.value}. La maquina inicia.",
                    )
                    mode = "playing"

    if mode == "menu":
        menu_buttons = draw_menu(screen, fonts, assets, mouse_pos)
    elif game_state:
        draw_game(screen, game_state, fonts, assets)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
