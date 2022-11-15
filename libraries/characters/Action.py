from libraries.Sound import *


class Action:

    def __init__(self, name, gif, sound=None):
        self.__name = name
        self.__gif = gif
        self.__sound_action = sound

    def play_sound_action(self, path=None):
        if self.__sound_action is not None:
            if path is not None:
                self.__sound_action(path)
            else:
                self.__sound_action()

    @property
    def name(self):
        return self.__name

    @property
    def gif(self):
        return self.__gif


ACTION_BACKWARD = Action('BACKWARD', 'backward.gif')
ACTION_FORWARD = Action('BACKWARD', 'forward.gif')
ACTION_BLOCK = Action('BLOCK', 'block.gif')
ACTION_NOTHING = Action('NOTHING', 'idle.gif')
ACTION_WIN = Action('WIN', 'win.gif', play_win)
ACTION_LOOSE = Action('LOOSE', 'ko.gif', play_loose)
