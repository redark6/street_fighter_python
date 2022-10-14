import pygame

from libraries.characters.Character import Character


class Guile(Character):
    CHARACTER_ANIMATION_PATH = 'guile/'
    CHARACTER_DEFAULT_WIDTH = 162
    CHARACTER_DEFAULT_HEIGHT = 200
    NAME = 'guile'

    def __init__(self, x, y, map, flip, is_player=False):
        super().__init__(x, y, map, flip, is_player)

    def actions(self, key):
        dx = 0
        if not self.is_acting and self.is_alive():
            if key[pygame.K_q]:
                dx = self.backward()
            elif key[pygame.K_d]:
                dx = self.forward()
            elif key[pygame.K_w] and not self.jumping:
                self.jump()
            elif key[pygame.K_r]:
                self.kick()
            elif key[pygame.K_t]:
                self.punch()
            elif key[pygame.K_y]:
                self.long_punch()
            elif key[pygame.K_u]:
                self.block_attack()
            else:
                if self.current_animation != 'idle.gif':
                    self.load_action_frame_list('idle.gif')
                    self.currentFrame = 0
        return dx
