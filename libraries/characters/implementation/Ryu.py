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
                if self.current_animation != 'idle.gif':
                    self.load_action_frame_list('idle.gif')
                    self.currentFrame = 0
        return dx
