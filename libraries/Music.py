import pygame


def load_and_play_bgm(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.set_volume(.2)
    pygame.mixer.music.play(-1)

def stop_bgm():
    pygame.mixer.music.stop()