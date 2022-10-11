import pygame


def loadLoadAndPlayBGM(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)