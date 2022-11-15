import pygame.display

from libraries.Map import Map
from libraries.Window import Window
from libraries.characters.implementation.Guile import Guile
from libraries.characters.implementation.Ryu import Ryu
from libraries.Sound import *
from libraries.Music import stop_bgm
import matplotlib.pyplot as plt
from random import *

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (237, 127, 20)
pygame.mixer.init(44100, -16, 2, 64)

FILE_RYU = 'ryu.al2'
FILE_GUILE = 'guile.al2'
# chose if we train ia or get previous train
LEARN_MODE = False
# chose if ia play or user
PLAYER_PLAY = True

def draw_bg_and_pass_it_to_next_frame():
    window.blit(map.get_current_frame(), map.get_current_frame_rect())
    map.pass_to_next_frame()


def draw_character_and_pass_it_to_next_frame(character):
    window.blit(character.get_flipped_current_frame(), character.get_current_frame_rect())
    character.pass_to_next_frame()


def draw_character_last_state(character):
    character.perform_last_animation()


def draw_character_final_msg(char1, char2):
    if (char1.is_player and not char2.is_player) or (not char1.is_player and char2.is_player):
        if not char1.is_alive() and not char2.is_alive():
            draw_text("Draw", count_font, RED, map.WIDTH / 2 - 120, map.HEIGHT / 3)
        elif (char1.is_player and char1.is_alive()) or char2.is_player and char2.is_alive():
            draw_text("Victory", count_font, RED, map.WIDTH / 2 - 120, map.HEIGHT / 3)
        elif (char1.is_player and not char1.is_alive()) or (char2.is_player and not char2.is_alive()):
            draw_text("Defeat", count_font, RED, map.WIDTH / 2 - 120, map.HEIGHT / 3)
    else:
        draw_text("Finish", count_font, RED, map.WIDTH / 2 - 120, map.HEIGHT / 3)


def draw_health_bar(health_ration, x, y):
    pygame.draw.rect(window.get_window(), WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(window.get_window(), RED, (x, y, 400, 30))
    pygame.draw.rect(window.get_window(), YELLOW, (x, y, 400 * health_ration, 30))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


def learn(player1, player2, iterations):
    for i in range(iterations):
        player1.reset(200, map.HEIGHT - 210)
        player2.reset(700, map.HEIGHT - 210)
        print("newgame " + str(i))
        while player1.is_alive() and player2.is_alive():
            player2.stepOne(None)
            player1.stepOne(None)
            player2.stepTwo()
            player1.stepTwo()


if __name__ == "__main__":
    # initialize game and window
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.init()
    count_font = pygame.font.Font("assets/fonts/street_fighter.ttf", 100)
    score_font = pygame.font.Font("assets/fonts/street_fighter.ttf", 30)
    intro_count = 4
    sound_count = 5
    round_over = False
    rounds = 0
    map = Map()

    guile = Guile(200, map.HEIGHT - 210, map, False, PLAYER_PLAY, True)
    ryu = Ryu(700, map.HEIGHT - 210, map, True, False, True)
    ryu.set_enemy(guile)
    guile.set_enemy(ryu)

    if LEARN_MODE:
        learn(guile, ryu, 1000)
    else:
        guile.load(FILE_GUILE)
        ryu.load(FILE_RYU)

    window = Window(map)
    ryu.set_train(False)
    guile.set_train(False)
    ryu.init_frame()
    guile.init_frame()

    map.load_map_frame_list()
    clock = pygame.time.Clock()
    last_count_update = pygame.time.get_ticks()
    end = False
    run = True

    while run:
        clock.tick(14)
        window.fill(0)
        events = pygame.event.get()

        if intro_count <= 0:
            draw_bg_and_pass_it_to_next_frame()

            if PLAYER_PLAY:
                ryu.stepOne(events)
                guile.perform_action(events)
                ryu.stepTwo()
            else:
                ryu.stepOne(events)
                guile.stepOne(events)
                ryu.stepTwo()
                guile.stepTwo()

        else:
            if clock.get_time() % 2 == 0:
                draw_bg_and_pass_it_to_next_frame()

            if intro_count == 1:
                draw_text("Fight !", count_font, RED, map.WIDTH / 2 - 120, map.HEIGHT / 2)
            else:
                draw_text(str(intro_count - 1), count_font, ORANGE, map.WIDTH / 2, map.HEIGHT / 2)

            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

            if (pygame.time.get_ticks() - last_count_update) >= 864:
                sound_count -= 1
                if sound_count == 4:
                    play_three()
                elif sound_count == 3:
                    play_two()
                elif sound_count == 2:
                    play_one()
                elif sound_count == 1:
                    play_fight()

        draw_health_bar(guile.get_hp_ratio(), 20, 20)
        draw_health_bar(ryu.get_hp_ratio(), 580, 20)
        draw_text("Guile:", score_font, RED, 20, 60)
        draw_text("Ryu:", score_font, RED, 580, 60)
        draw_character_and_pass_it_to_next_frame(guile)
        draw_character_and_pass_it_to_next_frame(ryu)

        if not round_over:
            if not guile.is_alive() or not ryu.is_alive():
                round_over = True
                round_over_time = pygame.time.get_ticks()
                guile.perform_last_sound()
                ryu.perform_last_sound()
                stop_bgm()
                play_ending()

        elif not end:
            draw_character_last_state(guile)
            draw_character_last_state(ryu)
            end = True
            #rounds += 1
            #round_over = False
            #guile.reset(200, map.HEIGHT - 210)
            #ryu.reset(700, map.HEIGHT - 210)
        else:
            draw_character_final_msg(guile, ryu)

        for event in events:
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()
    # end get inputs

    if not PLAYER_PLAY:
        guile.save(FILE_GUILE)
        ryu.save(FILE_RYU)

    plt.plot(guile.history)
    plt.plot(ryu.history)
    plt.show()
