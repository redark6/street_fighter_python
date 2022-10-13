import pygame

from libraries.gifLoader import loadGIF


class Character:
    BASE_ANIMATION_PATH = 'assets/characters'
    SPEED = 20
    GRAVITY = 5
    MAX_HEALTH = 100
    CHARACTER_DEFAULT_WIDTH = 162
    CHARACTER_DEFAULT_HEIGHT = 200

    def __init__(self, x, y, map):
        self.completedAnim = False
        self.characterActionFrameList = None
        self.enemy = None
        self.rect = pygame.Rect((x, y, self.CHARACTER_DEFAULT_WIDTH, self.CHARACTER_DEFAULT_HEIGHT))
        self.vel_y = 0
        self.map = map

        self.damage_ratio = 1

        self.jumping = False
        self.attacking = False
        self.flip = False
        self.is_acting = False

        # self.map_length = map_length
        self.hp = self.MAX_HEALTH
        self.currentFrame = 0
        self.load_action_frame_list("idle.gif")
        self.current_animation = "idle.gif"
        # self.position = positon

        # self.current_animation_path = self.animation_path + '/right/idle.gif'

    def load_action_frame_list(self, action):
        self.current_animation = action
        self.characterActionFrameList = loadGIF(self.BASE_ANIMATION_PATH + "/guile/" + action)

    def get_current_frame(self):
        return self.characterActionFrameList[self.currentFrame]

    def get_fliped_current_frame(self):
        return pygame.transform.flip(self.get_current_frame(), self.flip, False)

    def get_current_frame_rect(self):
        if self.attacking and self.flip:
            shift = self.rect.left - (self.get_current_frame().get_width() - self.CHARACTER_DEFAULT_WIDTH)
        else:
            shift = self.rect.left
        return self.get_fliped_current_frame().get_rect().move( shift , self.rect.top)

    # self.map.HEIGHT - self.get_current_frame().get_height() + self.rect.centery
    def pass_to_next_frame(self):
        self.currentFrame = (self.currentFrame + 1) % len(self.characterActionFrameList)

    def set_ennemy(self, enemy):
        self.enemy = enemy

    def get_hp_ratio(self):
        return self.hp / self.MAX_HEALTH

    def move(self, surface):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if self.is_acting:
            if self.characterActionFrameList[0] == self.get_current_frame():
                self.completedAnim = True
            if self.completedAnim:
                self.attacking = False
                self.is_acting = False
                self.load_action_frame_list('idle.gif')
                self.currentFrame = 0
                self.completedAnim = False

        if not self.is_acting:
            if key[pygame.K_q]:
                # self.is_acting = True
                dx -= self.SPEED
                self.load_action_frame_list('backward.gif')

            elif key[pygame.K_d]:
                # self.is_acting = True
                dx += self.SPEED
                self.load_action_frame_list('forward.gif')

            elif key[pygame.K_w] and not self.jumping:
                self.vel_y -= 35
                self.jumping = True
                # self.is_acting = True

            elif key[pygame.K_r]:
                self.is_acting = True
                self.load_action_frame_list('kick.gif')
                self.attack(surface)

            elif key[pygame.K_t]:
                self.is_acting = True
                self.load_action_frame_list('punch.gif')
                self.attack(surface)

            elif key[pygame.K_y]:
                self.is_acting = True
                self.load_action_frame_list('long_punch.gif')
                self.attack(surface)

            elif key[pygame.K_u]:
                self.is_acting = True
                self.damage_ratio = 0.5
                self.load_action_frame_list('block.gif')
                #self.attack(surface)
            else:
                if self.current_animation != 'idle.gif':
                    self.load_action_frame_list('idle.gif')
                    self.currentFrame = 0

        self.vel_y += self.GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = - self.rect.left
        if self.rect.right + dx > self.map.WIDTH:
            dx = self.map.WIDTH - self.rect.right

        if self.rect.bottom + dy > self.map.HEIGHT - 10:
            self.vel_y = 0
            self.jumping = False
            dy = self.map.HEIGHT - 10 - self.rect.bottom

        if self.enemy.get_rect().centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        self.rect.x += dx
        self.rect.y += dy

    def forward(self):
        return 0

    def backward(self):
        return 0

    def attack(self, surface):
        self.attacking = True

        if self.flip:
            shift = self.rect.left - (self.get_current_frame().get_width() - self.CHARACTER_DEFAULT_WIDTH)
        else:
            shift = self.rect.left

        frame = self.get_current_frame()
        attacking_rect = pygame.Rect(self.rect.centerx, shift, frame.get_width() - self.CHARACTER_DEFAULT_WIDTH,
                                     frame.get_height())
        if attacking_rect.colliderect(self.enemy.get_rect()):
            self.enemy.take_damage(10)
        pygame.draw.rect(surface, (0, 0, 255), attacking_rect)

    def get_rect(self):
        return self.rect

    def take_damage(self, damage):
        self.hp -= damage * self.damage_ratio

    def draw(self, surface):
        truc = 1
        #pygame.draw.rect(surface, (255, 0, 0), self.rect)


""""
    def evaluate_animation_direction(self):
    def idle(self):
    def move(self):
    def punch(self):
        self.changeAnimation('block', "right" if guile.position < 500 else "left")
    def long_punch(self):
    def kick(self):
    def parry(self):
"""


class Guile:
    def __init__(self, map_length):
        self.hp = 100
        self.animation_path = 'assets/characters/guile/'
        self.current_animation_path = self.animation_path + '/right/idle.gif'
        self.position = 0
        self.current_animation = 'idle'
        self.current_direction = 'right'
        self.map_length = map_length

    def loadAnim(self, anim):
        if anim == 'back':
            return 'back.gif'
        elif anim == 'block':
            return 'block.gif'
        elif anim == 'forward':
            return 'forward.gif'
        elif anim == 'idle':
            return 'idle.gif'
        elif anim == 'kick':
            return 'kick.gif'
        elif anim == 'long':
            return 'long.gif'
        elif anim == 'punch':
            return 'punch.gif'
        elif anim == 'win':
            return 'win.gif'

    def changeAnimation(self, anim, direction):
        loaded_animation = self.loadAnim(anim)
        self.current_animation_path = self.animation_path + direction + "/" + loaded_animation
        self.current_animation = anim
        self.current_direction = direction

    def takeDamage(self, amount):
        self.hp -= amount

    def move(self, pixel_change, image_width):
        future_position_left = self.position + pixel_change
        future_position_right = self.position + pixel_change + image_width
        if 0 < future_position_left < future_position_right < self.map_length:
            self.position += pixel_change


class Ryu:
    def __init__(self, map_length):
        self.hp = 100
        self.animation_path = 'assets/characters/ryu/'
        self.current_animation_path = self.animation_path + '/left/idle.gif'
        self.position = 900
        self.current_animation = 'idle'
        self.current_direction = 'left'
        self.map_length = map_length

    def loadAnim(self, anim):
        if anim == 'back':
            return 'back.gif'
        elif anim == 'block':
            return 'block.gif'
        elif anim == 'forward':
            return 'forward.gif'
        elif anim == 'idle':
            return 'idle.gif'
        elif anim == 'kick':
            return 'kick.gif'
        elif anim == 'long':
            return 'long.gif'
        elif anim == 'punch':
            return 'punch.gif'
        elif anim == 'win':
            return 'win.gif'

    def changeAnimation(self, anim, direction):
        loaded_animation = self.loadAnim(anim)
        self.current_animation_path = self.animation_path + direction + "/" + loaded_animation
        self.current_animation = anim
        self.current_direction = direction

    def takeDamage(self, amount):
        self.hp -= amount

    def move(self, pixel_change, image_width):
        future_position_left = self.position + pixel_change
        future_position_right = self.position + pixel_change + image_width
        if 0 < future_position_left < future_position_right < self.map_length:
            self.position += pixel_change
