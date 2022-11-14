from libraries.characters.Action import Action


class Attack(Action):

    def __init__(self, name, gif, damage, frame_mesures, surface_ratio, sound=None):
        super().__init__(name, gif, sound)
        self.__damage = damage
        self.__frame_width = frame_mesures[0]
        self.__frame_height = frame_mesures[1]
        self.__surface_ratio = surface_ratio

    @property
    def damage(self):
        return self.__damage

    @property
    def frame_width(self):
        return self.__frame_width

    @property
    def frame_height(self):
        return self.__frame_height

    @property
    def surface_ratio(self):
        return self.__surface_ratio
