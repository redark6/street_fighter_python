class Guile:
    def __init__(self):
        self.hp = 100
        self.animation_path = 'assets/characters/guile/'
        self.current_animation_path = self.animation_path + 'right_idle_2.gif'
        self.position = 40
        self.previous_anim = 'right_idle'
        self.current_animation = 'right_idle'

    def loadAnim(self, anim):
        if anim == 'right_idle' :
            return 'right_idle_2.gif'
        else :
            return 'left_idle.gif'

    def changeAnimation(self, anim):
        loaded_animation = self.loadAnim(anim)
        self.current_animation_path = self.animation_path + loaded_animation
        self.current_animation = anim

    def takeDamage(self, amount):
        self.hp -= amount

    def move(self, pixel_change):
        self.position += pixel_change

