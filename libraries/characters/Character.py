import pygame

import pickle
from random import *

from libraries.characters.AnimationSoundHelper import AnimationSoundHelper
from libraries.characters.Action import *
from libraries.characters.Attack import Attack


def get_state_from_int(number):
    return False if number == 0 else True


class Character:
    ATTACK_PUNCH = Attack('PUNCH', 'punch.gif', 10, (174, 200), 0.4, play_punch)
    ATTACK_KICK = Attack('KICK', 'kick.gif', 15, (113, 200), 0.6, play_kick)
    ATTACK_LONG_PUNCH = Attack('LONG_PUNCH', 'long_punch.gif', 20, (326, 200), 0.8, play_long_punch)

    BACKWARD = 'BACKWARD'
    FORWARD = 'FORWARD'
    JUMP = 'JUMP'
    BLOCK = 'BLOCK'
    PUNCH = 'PUNCH'
    KICK = 'KICK'
    LONG_PUNCH = 'LONG_PUNCH'
    NOTHING = 'NOTHING'

    ACTIONS = [BACKWARD, FORWARD, JUMP, BLOCK, PUNCH, KICK, LONG_PUNCH, NOTHING]

    HEAT_LOOSE_THRESHOLD = 30

    BASE_ANIMATION_PATH = 'assets/characters/'
    CHARACTER_ANIMATION_PATH = 'todefine/'
    NAME = ''
    SPEED = 20
    GRAVITY = 7
    MAX_HEALTH = 100
    CHARACTER_DEFAULT_WIDTH = 162
    CHARACTER_DEFAULT_HEIGHT = 200

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
    else:
        joystick = False

    def __init__(self, x, y, map, flip, is_player=False, train=False, alpha=0.001, gamma=0.2, cooling_rate=0.3):
        self.completedAnim = False
        self.enemy = None
        self.hit_box = pygame.Rect((x, y, self.CHARACTER_DEFAULT_WIDTH, self.CHARACTER_DEFAULT_HEIGHT))
        self.vel_y = 0
        self.map = map
        self.is_player = is_player
        self.__train = train
        self.damage_ratio = 1
        self.successive_loose = 0
        self.animation_sound_helper = AnimationSoundHelper(self.BASE_ANIMATION_PATH + self.CHARACTER_ANIMATION_PATH,
                                                           self.CHARACTER_DEFAULT_WIDTH)
        self.jumping = False
        self.attacking = False
        self.flip = flip
        self.is_acting = False
        self.party_finish = False

        self.hp = self.MAX_HEALTH
        self.play_action(ACTION_NOTHING)

        self.__state = (False, False, False, False, False, False, False, False, False)
        self.__score = 0
        self.__temperature = 0
        self.__temp_reward = 0

        self.__radar = (False, False, False, False, False, False, False)
        self.init_q_table()
        self.__reward_kill = self.MAX_HEALTH * 5
        self.__reward_death = self.MAX_HEALTH * -100

        self.reset(x, y, False)
        self.__alpha = alpha
        self.__gamma = gamma
        self.__cooling_rate = cooling_rate
        self.__history = []
        self.__last_action = None
        self.__action_counter = 0
        self.__special_move_accumulator = 0

    def get_flipped_current_frame(self):
        return self.animation_sound_helper.get_flipped_current_frame(self.flip)

    def get_current_frame_rect(self):
        return self.animation_sound_helper.get_current_frame_rect(self.hit_box, self.attacking, self.flip)

    def pass_to_next_frame(self):
        self.animation_sound_helper.pass_to_next_frame(self.party_finish)

    # function to get player status
    def is_alive(self):
        return self.hp > 0

    def set_enemy(self, enemy):
        self.enemy = enemy
        self.previous_ennemy_hp = self.enemy.hp


    def get_hp_ratio(self):
        return self.hp / self.MAX_HEALTH

    def get_hit_box(self):
        return self.hit_box

    def refresh_radar(self):
        (x, y) = self.hit_box.bottomleft
        radar_item = pygame.Rect((x - self.CHARACTER_DEFAULT_WIDTH, y, self.CHARACTER_DEFAULT_WIDTH * 3,
                                  self.CHARACTER_DEFAULT_HEIGHT * 1.5))

        r = True if radar_item.colliderect(self.enemy.get_hit_box()) else False
        ph = self.will_attack_hit(self.ATTACK_PUNCH)
        kh = self.will_attack_hit(self.ATTACK_KICK)
        sh = self.will_attack_hit(self.ATTACK_LONG_PUNCH)
        rp = self.enemy.will_attack_hit(self.enemy.ATTACK_PUNCH)
        rk = self.enemy.will_attack_hit(self.enemy.ATTACK_KICK)
        rs = self.enemy.will_attack_hit(self.enemy.ATTACK_LONG_PUNCH)

        self.__radar = (r, kh, ph, sh, rk, rp, rs)

    def init_q_table(self):
        self.__qtable = {}
        for is_jumping in range(0, 2):
            for is_before_enemy in range(0, 2):
                for is_in_radar in range(0, 2):
                    for punch_can_hit in range(0, 2):
                        for kick_can_hit in range(0, 2):
                            for super_punch_can_hit in range(0, 2):
                                for is_reachable_punch in range(0, 2):
                                    for is_reachable_kick in range(0, 2):
                                        for is_reachable_super_punch in range(0, 2):
                                            j = get_state_from_int(is_jumping)
                                            b = get_state_from_int(is_before_enemy)
                                            r = get_state_from_int(is_in_radar)
                                            ph = get_state_from_int(punch_can_hit)
                                            kh = get_state_from_int(kick_can_hit)
                                            sh = get_state_from_int(super_punch_can_hit)
                                            rp = get_state_from_int(is_reachable_punch)
                                            rk = get_state_from_int(is_reachable_kick)
                                            rs = get_state_from_int(is_reachable_super_punch)
                                            self.__qtable[(j, b, r, ph, kh, sh, rp, rk, rs)] = {}
                                            for action in self.ACTIONS:
                                                self.__qtable[(j, b, r, ph, kh, sh, rp, rk, rs)][action] = 0.0

    def perform_action(self, events, key=None, train=False):
        dy = 0
        if not train:
            key = pygame.key.get_pressed()
        if self.is_acting:
            if self.is_current_frame_first():
                self.completedAnim = True
                self.animation_sound_helper.reset_current_frame_position()
            if self.completedAnim:
                self.attacking = False
                self.is_acting = False
                self.damage_ratio = 1
                self.play_action(ACTION_NOTHING)
                self.completedAnim = False

        if not self.party_finish:
            if not train:
                dx = self.actions(key, events)
            else:
                dx = self.actions_train(key)
        else:
            dx = 0

        self.vel_y += self.GRAVITY
        dy += self.vel_y

        if self.hit_box.left + dx < 0:
            dx = - self.hit_box.left
            self.punish_player(200)

        if self.hit_box.right + dx > self.map.WIDTH:
            dx = self.map.WIDTH - self.hit_box.right
            self.punish_player(200)

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

    def die(self):
        self.play_action(ACTION_LOOSE)

    def win(self):
        self.play_action(ACTION_WIN)

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

    def take_damage(self, damage):
        self.punish_player((damage * 50))
        if self.damage_ratio != 1:
            self.reward_player(damage * self.damage_ratio)
        self.hp -= damage * self.damage_ratio

    def block_attack(self):
        self.is_acting = True
        self.damage_ratio = 0.5
        self.play_action(ACTION_BLOCK)
        self.punish_player(10)

    def forward(self):
        if self.flip:
            self.play_action(ACTION_BACKWARD)
        else:
            self.play_action(ACTION_FORWARD)
        return self.SPEED

    def backward(self):
        if self.flip:
            self.play_action(ACTION_FORWARD)
        else:
            self.play_action(ACTION_BACKWARD)
        return - self.SPEED

    def jump(self):
        self.vel_y -= 35
        self.jumping = True

    def punch(self):
        self.play_action(self.ATTACK_PUNCH)
        self.attack(self.ATTACK_PUNCH)

    def kick(self):
        self.play_action(self.ATTACK_KICK)
        self.attack(self.ATTACK_KICK)

    def long_punch(self):
        self.play_action(self.ATTACK_LONG_PUNCH, self.NAME)
        self.attack(self.ATTACK_LONG_PUNCH)

    def attack(self, attack):
        self.__special_move_accumulator += attack.damage
        self.attacking = True
        self.is_acting = True
        if self.will_attack_hit(attack):
            self.enemy.take_damage(attack.damage)
            self.reward_player(attack.damage)
        else:
            self.punish_player(attack.damage)

    def set_surface(self, surface):
        self.surface = surface
    def will_attack_hit(self, attack):
        shift = self.hit_box.left - (
                    attack.frame_width - self.CHARACTER_DEFAULT_WIDTH) if self.flip else self.hit_box.right
        attacking_rect = pygame.Rect(shift, self.hit_box.top, attack.frame_width - self.CHARACTER_DEFAULT_WIDTH,
                                     attack.frame_height * attack.surface_ratio)
        return attacking_rect.colliderect(self.enemy.get_hit_box())

    def reward_player(self, reward):
        self.__temp_reward += reward

    def punish_player(self, punishment):
        self.__temp_reward -= punishment

    def reset_player_reward(self):
        self.__temp_reward = 0

    def stepOne(self, event):
        self.reset_player_reward()
        self.__temp_action = None
        self.__temp_state = None
        if not self.party_finish:
            action = self.best_action()
            state, reward = self.do(event, action)
            self.__temp_action = action
            self.reward_player(reward)
            self.__temp_state = state

    def stepTwo(self):
        if not self.party_finish:
            reward = self.__temp_reward

            if not self.is_alive():
                reward += -10000
                self.successive_loose += 1
                self.party_finish = True

            if not self.enemy.is_alive():
                reward += 1000
                self.successive_loose = 0
                self.party_finish = True

            action = self.__temp_action
            state = self.__temp_state
            maxQ = max(self.__qtable[state].values())
            delta = self.__alpha * (reward + self.__gamma * maxQ - self.__qtable[self.__state][action])
            self.__qtable[self.__state][action] += delta

            self.__state = state
            self.__score += reward

            return action, reward

    def best_action(self):
        if random() < self.__temperature:
            #print("cooling ")
            #print(self.__temperature)
            self.__temperature *= self.__cooling_rate
            return choice(self.ACTIONS)
        else:
            q = self.__qtable[self.__state]
            return max(q, key=q.get)

    def do(self, event, action):
        self.heat_character_if_threshold_exceed()
        self.refresh_radar()
        self.perform_action(event, action, True)

        new_state = (
            self.jumping,
            self.flip,
            self.__radar[0],
            self.__radar[1],
            self.__radar[2],
            self.__radar[3],
            self.__radar[4],
            self.__radar[5],
            self.__radar[6]
        )

        reward = -1
        #if(self.__last_action=='idle.gif')
            #reward -= self.__action_counter
        return new_state, reward

    def heat(self):
        self.__temperature = 1

    def heat_character_if_threshold_exceed(self):
        if self.successive_loose > self.HEAT_LOOSE_THRESHOLD:
            #print("heat " + self.NAME)
            self.heat()
            self.successive_loose = 0

    def load(self, filename):
        with open(filename, 'rb') as file:
            self.__qtable, self.__history = pickle.load(file)

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__qtable, self.__history), file)

    def reset(self, x, y, append_score=True):
        if append_score:
            self.__history.append(self.__score)
        self.__state = (False, False, False, False, False, False, False, False, False)
        self.__score = 0
        self.__temperature = 0
        self.hp = self.MAX_HEALTH
        self.hit_box = pygame.Rect((x, y, self.CHARACTER_DEFAULT_WIDTH, self.CHARACTER_DEFAULT_HEIGHT))
        self.party_finish = False

    def actions_train(self, key):
        #print(key)
        dx = 0
        if not self.is_acting and self.is_alive():
            self.__action_counter += 1
            if self.__action_counter % 200 == 0 and self.enemy.hp == self.previous_ennemy_hp :
                print("heat " +self.NAME)
                self.heat()
            elif self.__action_counter % 200 == 0 :
                self.previous_ennemy_hp =  self.enemy.hp

            if key == self.BACKWARD:
                dx = self.backward()
            elif key == self.FORWARD:
                dx = self.forward()
            elif key == self.JUMP:
                if not self.jumping:
                    self.jump()
                    self.punish_player(5)
                else:
                    self.punish_player(20)
            elif key == self.KICK:
                self.kick()
            elif key == self.PUNCH:
                self.punch()
            elif key == self.LONG_PUNCH:
                if self.__special_move_accumulator <= (self.ATTACK_LONG_PUNCH.damage * 3):
                    return dx
                self.long_punch()
                self.__special_move_accumulator = 0
            elif key == self.BLOCK:
                self.block_attack()
            else:
                self.reset_animation()

        return dx


    def reset_animation(self):
        if not self.__train:
            self.animation_sound_helper.reset_animation()

    def play_action(self, action, path=None):
        if not self.__train:
            self.animation_sound_helper.play_action(action, path)

    def is_current_frame_first(self):
        if not self.__train:
            return self.animation_sound_helper.is_current_frame_first()
        else:
            return True

    def set_train(self, train):
        self.__train = train

    def init_frame(self):
        self.play_action(ACTION_NOTHING)

    @property
    def score(self):
        return self.__score

    @property
    def history(self):
        return self.__history
