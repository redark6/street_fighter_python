import pygame

from libraries.characters.Character import Character


class Guile(Character):
    CHARACTER_ANIMATION_PATH = 'guile/'
    CHARACTER_DEFAULT_WIDTH = 162
    CHARACTER_DEFAULT_HEIGHT = 200
    NAME = 'guile'

    left_control = False
    right_control = False
    punch_control = False
    kick_control = False
    special_control = False
    jump_control = False
    parade_control = False
    def __init__(self, x, y, map, flip, is_player=False):
        super().__init__(x, y, map, flip, is_player)

    def actions(self, key, events):
        dx = 0
        if self.joystick:
            self.controler(events)
        if not self.is_acting and self.is_alive():
            if key[pygame.K_q] or self.left_control:
                dx = self.backward()
            elif key[pygame.K_d] or self.right_control:
                dx = self.forward()
            elif (key[pygame.K_w] or self.jump_control) and not self.jumping:
                self.jump()
            elif key[pygame.K_r] or self.kick_control:
                self.kick()
            elif key[pygame.K_t] or self.punch_control:
                self.punch()
            elif key[pygame.K_y] or self.special_control:
                self.long_punch()
                if self.joystick:
                    self.joystick.rumble(10000000, 1000000, 400)
            elif key[pygame.K_u] or self.parade_control:
                self.block_attack()
            else:
                if self.current_animation != 'idle.gif':
                    self.load_action_frame_list('idle.gif')
                    self.currentFrame = 0
        return dx

    def take_damage(self, damage):
        self.hp -= damage * self.damage_ratio
        if self.joystick:
            self.joystick.rumble(100, 100, 300)

    def controler(self, events):
        self.punch_control = False
        self.jump_control = False
        self.kick_control = False
        self.special_control = False
        self.parade_control = False

        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(1):
                    self.punch_control = True
                    #b
                if self.joystick.get_button(0):
                    #a
                    self.jump_control = True
                if self.joystick.get_button(2):
                    #x
                    self.kick_control = True
                if self.joystick.get_button(3):
                    #y
                    self.special_control = True
                if self.joystick.get_button(5):
                    #rt
                    self.parade_control = True

        if self.joystick.get_axis(0) == -1:
            self.left_control = True
            self.right_control = False
        elif self.joystick.get_axis(0) > 0.9:
            self.right_control = True
            self.left_control = False
        else:
            self.right_control = False
            self.left_control = False