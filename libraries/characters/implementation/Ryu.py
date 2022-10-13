from libraries.characters.Character import Character

class Ryu(Character):

    character_animation_path = 'ryu'

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