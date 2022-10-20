import pygame

from libraries.characters.Character import Character


class Ryu(Character):
    CHARACTER_ANIMATION_PATH = 'ryu/'
    CHARACTER_DEFAULT_WIDTH = 108
    CHARACTER_DEFAULT_HEIGHT = 200
    NAME = 'ryu'

    def __init__(self, x, y, map, flip, is_player=False):
        super().__init__(x, y, map, flip, is_player)

    def actions(self, key, events):
        if self.distance() < 162:
            dx = self.forward()
        else:
            dx = self.backward()

        return dx
