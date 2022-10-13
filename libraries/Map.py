from libraries.gifLoader import loadGIF
from libraries.music import load_and_play_bgm


class Map:
    WIDTH = 1000
    HEIGHT = 440

    def __init__(self):
        self.mapFrameList = None
        self.currentFrame = 0
        load_and_play_bgm("assets/audio/map-stages/air-force-base.mp3")

    def load_map_frame_list(self):
        self.mapFrameList = loadGIF("assets/map/air-force-base.gif")

    def get_current_frame(self):
        return self.mapFrameList[self.currentFrame]

    def get_current_frame_rect(self):
        return self.get_current_frame().get_rect()

    def pass_to_next_frame(self):
        self.currentFrame = (self.currentFrame + 1) % len(self.mapFrameList)
