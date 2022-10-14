import pygame

from libraries.GifLoader import load_gif
from libraries.Sound import *


class Character:
    BASE_ANIMATION_PATH = 'assets/characters/'
    CHARACTER_ANIMATION_PATH = 'todefine/'
    NAME = ''
    SPEED = 20
    GRAVITY = 5
    MAX_HEALTH = 100
    CHARACTER_DEFAULT_WIDTH = 162
    CHARACTER_DEFAULT_HEIGHT = 200

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
    else:
        joystick = False
    def __init__(self, x, y, map, flip, is_player=False):
        self.completedAnim = False
        self.characterActionFrameList = None
        self.enemy = None
        self.hit_box = pygame.Rect((x, y, self.CHARACTER_DEFAULT_WIDTH, self.CHARACTER_DEFAULT_HEIGHT))
        self.vel_y = 0
        self.map = map
        self.is_player = is_player

        self.damage_ratio = 1

        self.jumping = False
        self.attacking = False
        self.flip = flip
        self.is_acting = False
        self.party_finish = False

        self.hp = self.MAX_HEALTH
        self.currentFrame = 0
        self.load_action_frame_list("idle.gif")
        self.current_animation = "idle.gif"

    # functions used to display player
    def load_action_frame_list(self, action):
        self.current_animation = action
        self.characterActionFrameList = load_gif(self.BASE_ANIMATION_PATH + self.CHARACTER_ANIMATION_PATH + action)

    def get_current_frame(self):
        return self.characterActionFrameList[self.currentFrame]

    def get_fliped_current_frame(self):
        return pygame.transform.flip(self.get_current_frame(), self.flip, False)

    def get_current_frame_rect(self):
        if self.attacking and self.flip:
            shift = self.hit_box.left - (self.get_current_frame().get_width() - self.CHARACTER_DEFAULT_WIDTH)
        else:
            shift = self.hit_box.left
        return self.get_fliped_current_frame().get_rect().move(shift, self.hit_box.top)

    def pass_to_next_frame(self):
        if self.party_finish and self.currentFrame == len(self.characterActionFrameList) - 1 and \
                (self.current_animation == "win.gif" or self.current_animation == "ko.gif"):
            self.currentFrame = len(self.characterActionFrameList) - 1
        else:
            self.currentFrame = (self.currentFrame + 1) % len(self.characterActionFrameList)

    # function to get player status
    def is_alive(self):
        return self.hp > 0

    def set_ennemy(self, enemy):
        self.enemy = enemy

    def get_hp_ratio(self):
        return self.hp / self.MAX_HEALTH

    def get_hit_box(self):
        return self.hit_box

    def perform_action(self, events):
        dy = 0
        key = pygame.key.get_pressed()

        if self.is_acting:
            if self.characterActionFrameList[0] == self.get_current_frame():
                self.completedAnim = True
            if self.completedAnim:
                self.attacking = False
                self.is_acting = False
                self.damage_ratio = 1
                self.load_action_frame_list('idle.gif')
                self.currentFrame = 0
                self.completedAnim = False

        if not self.party_finish:
            dx = self.actions(key, events)
        else:
            dx = 0

        self.vel_y += self.GRAVITY
        dy += self.vel_y

        if self.hit_box.left + dx < 0:
            dx = - self.hit_box.left
        if self.hit_box.right + dx > self.map.WIDTH:
            dx = self.map.WIDTH - self.hit_box.right

        if self.hit_box.bottom + dy > self.map.HEIGHT - 10:
            self.vel_y = 0
            self.jumping = False
            dy = self.map.HEIGHT - 10 - self.hit_box.bottom

        if self.enemy.get_hit_box().centerx > self.hit_box.centerx:
            self.flip = False
        else:
            self.flip = True

        self.hit_box.x += dx
        self.hit_box.y += dy

    def perform_last_animation(self):
        self.party_finish = True
        if self.is_alive():
            self.win()
        else:
            self.die()

    def perform_last_sound(self):
        if self.is_player:
            if self.is_alive():
                play_win()
            else:
                play_loose()

    def actions(self, key, event):
        dx = 0
        print("you should define this function for each character implementation")
        return dx

    def die(self):
        self.load_action_frame_list('ko.gif')

    def win(self):
        self.load_action_frame_list('win.gif')

    def take_damage(self, damage):
        self.hp -= damage * self.damage_ratio

    # players actions
    def block_attack(self):
        self.damage_ratio = 0.5
        self.load_action_frame_list('block.gif')
        self.is_acting = True

    def forward(self):
        if self.flip:
            self.load_action_frame_list('backward.gif')
        else:
            self.load_action_frame_list('forward.gif')
        return self.SPEED

    def backward(self):
        if self.flip:
            self.load_action_frame_list('forward.gif')
        else:
            self.load_action_frame_list('forward.gif')
        return - self.SPEED

    def jump(self):
        self.vel_y -= 35
        self.jumping = True

    def kick(self):
        play_kick()
        self.load_action_frame_list('kick.gif')
        self.attack(15, 0.6)

    def punch(self):
        play_punch()
        self.load_action_frame_list('punch.gif')
        self.attack(10, 0.4)

    def long_punch(self):
        play_long_punch(self.NAME)
        self.load_action_frame_list('long_punch.gif')
        self.attack(20, 0.8)

    def attack(self, damage, attack_surface_ratio):
        self.attacking = True
        self.is_acting = True
        frame = self.get_current_frame()

        if self.flip:
            shift = self.hit_box.left - (self.get_current_frame().get_width() - self.CHARACTER_DEFAULT_WIDTH)
        else:
            shift = self.hit_box.right

        attacking_rect = pygame.Rect(shift, self.hit_box.top, frame.get_width() - self.CHARACTER_DEFAULT_WIDTH,
                                     frame.get_height() * attack_surface_ratio)
        if attacking_rect.colliderect(self.enemy.get_hit_box()):
            self.enemy.take_damage(damage)
