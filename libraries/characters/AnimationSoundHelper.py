import pygame

from libraries.GifLoader import load_gif
from libraries.characters.Action import ACTION_NOTHING


class AnimationSoundHelper:

    def __init__(self, base_animation_path, character_default_width):
        self.__base_animation_path = base_animation_path
        self.__character_default_width = character_default_width
        self.__current_animation = None
        self.__character_action_frameList = None
        self.__current_frame_position = 0
#        self.play_action(ACTION_NOTHING)

    def load_action_frame_list(self, action):
        self.__current_animation = action.gif
        self.__character_action_frame_list = load_gif(self.__base_animation_path + action.gif)

    def play_action(self, action, path=None, is_player = False):
        if action.name == "WIN" or action.name == "LOOSE" and not is_player:
            print("no loose or win for bot")
        else:
            action.play_sound_action(path)
        self.load_action_frame_list(action)

    def get_current_frame(self):
        if self.__current_frame_position > len(self.__character_action_frame_list) - 1:
            self.__current_frame_position = len(self.__character_action_frame_list) - 1
        return self.__character_action_frame_list[self.__current_frame_position]

    def get_flipped_current_frame(self, flip):
        return pygame.transform.flip(self.get_current_frame(), flip, False)

    def get_current_frame_rect(self, character_hit_box, attacking, flip):
        if attacking and flip:
            shift = character_hit_box.left - (
                    self.get_current_frame().get_width() - self.__character_default_width)
        else:
            shift = character_hit_box.left
        return self.get_flipped_current_frame(flip).get_rect().move(shift, character_hit_box.top)

    def pass_to_next_frame(self, party_finish):
        if party_finish and self.__current_frame_position == len(self.__character_action_frame_list) - 1 and \
                (self.__current_animation == "win.gif" or self.__current_animation == "ko.gif"):
            self.__current_frame_position = len(self.__character_action_frame_list) - 1
        else:
            self.__current_frame_position = (self.__current_frame_position + 1) % len(
                self.__character_action_frame_list)
            if self.__current_frame_position > len(self.__character_action_frame_list) - 1:
                self.__current_frame_position = len(self.__character_action_frame_list) - 1

    def is_current_frame_first(self):
        return self.__character_action_frame_list[0] == self.get_current_frame()

    def reset_animation(self):
        if self.__current_animation != ACTION_NOTHING.gif:
            self.play_action(ACTION_NOTHING)

    def reset_current_frame_position(self):
        self.__current_frame_position = 0
