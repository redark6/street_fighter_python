class Guile:
    def __init__(self):
        self.hp = 100
        self.animation_path = 'assets/characters/guile/'
        self.current_animation_path = self.animation_path + '/right/idle.gif'
        self.position = 40
        self.previous_anim = 'right_idle'
        self.current_animation = 'right_idle'
        self.current_direction = 'right'

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

    def move(self, pixel_change):
        self.position += pixel_change

