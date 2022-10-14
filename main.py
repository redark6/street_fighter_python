import pygame.display

from libraries.Map import Map
from libraries.Window import Window
from libraries.characters.implementation.Guile import Guile
from libraries.characters.implementation.Ryu import Ryu
from libraries.gifLoader import *

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (237, 127, 20)


def draw_bg_and_pass_it_to_next_frame():
    window.blit(map.get_current_frame(), map.get_current_frame_rect())
    map.pass_to_next_frame()


def draw_character_and_pass_it_to_next_frame(character):
    window.blit(character.get_fliped_current_frame(), character.get_current_frame_rect())
    character.pass_to_next_frame()


def draw_character_last_state(character):
    character.perform_last_animation()


def draw_health_bar(health_ration, x, y):
    pygame.draw.rect(window.get_window(), WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(window.get_window(), RED, (x, y, 400, 30))
    pygame.draw.rect(window.get_window(), YELLOW, (x, y, 400 * health_ration, 30))


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


if __name__ == "__main__":
    # initialize game and window
    pygame.init()
    count_font = pygame.font.Font("assets/fonts/street_fighter.ttf", 100)
    score_font = pygame.font.Font("assets/fonts/street_fighter.ttf", 30)
    intro_count = 4
    round_over = False

    map = Map()
    window = Window(map)
    map.load_map_frame_list()
    clock = pygame.time.Clock()
    last_count_update = pygame.time.get_ticks()

    guile = Guile(200, map.HEIGHT - 210, map, False)
    ryu = Ryu(700, map.HEIGHT - 210, map, True)
    ryu.set_ennemy(guile)
    guile.set_ennemy(ryu)

    run = True

    while run:
        clock.tick(14)
        window.fill(0)

        if intro_count <= 0:
            draw_bg_and_pass_it_to_next_frame()
            guile.perform_action()
            ryu.perform_action()
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

        draw_health_bar(guile.get_hp_ratio(), 20, 20)
        draw_health_bar(ryu.get_hp_ratio(), 580, 20)
        draw_text("Guile:", score_font, RED, 20, 60)
        draw_text("Ryu:", score_font, RED, 580, 60)
        draw_character_and_pass_it_to_next_frame(guile)
        draw_character_and_pass_it_to_next_frame(ryu)

        if not round_over:
            if not guile.is_alive() or not ryu.is_alive():
                # score[1] += 1
                # score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            draw_text("Victory", count_font, RED, map.WIDTH / 2 - 120, map.HEIGHT / 2)
            draw_character_last_state(guile)
            draw_character_last_state(ryu)
            # if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            # round_over = False
            # intro_count = 3
            # fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            # fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.flip()
    # end get inputs
