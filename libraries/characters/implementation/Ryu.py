import pygame

from libraries.Sound import *
from libraries.characters.Attack import Attack
from libraries.characters.Character import Character


class Ryu(Character):
    ATTACK_PUNCH = Attack('PUNCH', 'punch.gif', 10, (164, 200), 0.4, play_punch)
    ATTACK_KICK = Attack('KICK', 'kick.gif', 15, (213, 200), 0.6, play_kick)
    ATTACK_LONG_PUNCH = Attack('LONG_PUNCH', 'long_punch.gif', 20, (326, 200), 0.8, play_long_punch)

    #ATTACK_PUNCH = Attack('PUNCH', 'punch.gif', 10, (310, 200), 0.4, play_punch)
    #ATTACK_KICK = Attack('KICK', 'kick.gif', 15, (233, 200), 0.6, play_kick)
    #ATTACK_LONG_PUNCH = Attack('LONG_PUNCH', 'long_punch.gif', 20, (440, 200), 0.8, play_long_punch)


    CHARACTER_ANIMATION_PATH = 'ryu/'
    CHARACTER_DEFAULT_WIDTH = 108
    CHARACTER_DEFAULT_HEIGHT = 200
    NAME = 'ryu'

    def __init__(self, x, y, map, flip, is_player=False, train=False):
        super().__init__(x, y, map, flip, is_player, train)

    def actions(self, key, events):
        dx = 0
        if not self.is_acting and self.is_alive():
            if key[pygame.K_RIGHT]:
                dx = self.backward()
            elif key[pygame.K_LEFT]:
                dx = self.forward()
            elif key[pygame.K_UP] and not self.jumping:
                self.jump()
            elif key[pygame.K_c]:
                self.kick()
            elif key[pygame.K_v]:
                self.punch()
            elif key[pygame.K_b]:
                self.long_punch()
            elif key[pygame.K_DOWN]:
                self.block_attack()
            else:
                self.animation_sound_helper.reset_animation()

        return dx
