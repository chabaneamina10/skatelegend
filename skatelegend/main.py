
import pygame
import math,sys
from ui import (particules, MenuScreen, ConfigScreen, GameScreen, ResultsScreen,init_fonts)

# Configuration du chemin des assets
ASSETS_PATH = "../assets" 
W, H = 1280, 720
FPS = 60
S_MENU, S_CONFIG, S_GAME, S_RESULTS = "menu", "config", "game", "results"

def main():
    pygame.init()
    pygame.display.set_caption("Skate Legend")
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    fonts = init_fonts()
    state = S_MENU
    current = MenuScreen(screen, fonts)
    config_screen = None
    game_screen = None
    results_screen = None
    
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            result = current.handle_event(ev)
            if result == S_MENU:
                state = S_MENU
                current = MenuScreen(screen, fonts)
            elif result == S_CONFIG:
                state = S_CONFIG
                config_screen = ConfigScreen(screen, fonts)
                current = config_screen
            elif result == S_GAME:
                if config_screen:
                    names, humans = config_screen.get_config()
                    state = S_GAME
                    game_screen = GameScreen(screen, fonts, names, humans)
                    # Lancer le jeu 
                    next_state,vainqueur,scores = game_screen.play()
                    if next_state == S_RESULTS:
                        state = S_RESULTS
                        results_screen = ResultsScreen(screen, fonts,vainqueur,scores)
                        current = results_screen
            elif result == S_RESULTS:
                state = S_RESULTS
                current = results_screen
        
        if hasattr(current, "update"):
            current.update()
        current.draw()
        pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    main()
