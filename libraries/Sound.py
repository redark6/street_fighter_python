import pygame

BASE_SOUND_PATH = 'assets/sounds/'


def load_and_play_sound(filename):
    sound_effect = pygame.mixer.Sound(BASE_SOUND_PATH + filename)
    sound_effect.play()


def play_punch():
    load_and_play_sound("common/punch.mp3")


def play_kick():
    load_and_play_sound("common/kick.mp3")


def play_long_punch(character_name):
    load_and_play_sound(character_name + "/long_punch.mp3")


def play_loose():
    load_and_play_sound("common/loose.mp3")


def play_win():
    load_and_play_sound("common/win.mp3")


def play_one():
    load_and_play_sound("common/one.mp3")


def play_two():
    load_and_play_sound("common/two.mp3")


def play_three():
    load_and_play_sound("common/three.mp3")


def play_fight():
    load_and_play_sound("common/fight.mp3")
