import pygame
def play_sound():

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("../sound/swipe.mp3")
    pygame.mixer.music.play()
