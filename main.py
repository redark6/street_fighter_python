import pygame.display
from pygame import *

from libraries.Map import Map
from libraries.Window import Window
from libraries.characters.Character import Character
from libraries.characters.implementation import Ryu, Guile
from libraries.gifLoader import *
from libraries.music import load_and_play_bgm

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 440

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


def countKeyPressed(keys):
    return sum(x == True for x in keys)


if __name__ == "__main__":
    # initialize game and window
    pygame.init()

    map = Map()
    window = Window(map)
    map.load_map_frame_list()

    clock = pygame.time.Clock()

    # mapFrameList = loadGIF("assets/map/air-force-base.gif")
    # guile = Guile(1000)
    # currentFrame = 0
    # currentGuileFrame = 0

    # ryu = Ryu(1000)
    # currentRyuFrame = 0
    guile = Character(200, 430, map)
    ryu = Character(700, 430, map)
    ryu.set_ennemy(guile)
    guile.set_ennemy(ryu)
    run = True

    # guile_anim = loadGIF(guile.current_animation_path)
    # ryu_anim = loadGIF(ryu.current_animation_path)

    """
    animating = 0
    count = 0
    completedAnim = False
 """


    def draw_bg_and_pass_it_to_next_frame():
        window.blit(map.get_current_frame(), map.get_current_frame_rect())
        map.pass_to_next_frame()

    def draw_character_and_pass_it_to_next_frame():
        window.blit(guile.get_fliped_current_frame(), guile.get_current_frame_rect())
        guile.pass_to_next_frame()

    def draw_character_and_pass_it_to_next_frame_2():
        window.blit(ryu.get_fliped_current_frame(), ryu.get_current_frame_rect())
        ryu.pass_to_next_frame()

    def draw_health_bar(health_ration, x, y):
        pygame.draw.rect(window.get_window(), WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(window.get_window(), RED, (x, y, 400, 30))
        pygame.draw.rect(window.get_window(), YELLOW, (x, y, 400 * health_ration, 30))


    while run:
        clock.tick(14)
        window.fill(0)

        draw_bg_and_pass_it_to_next_frame()
        draw_character_and_pass_it_to_next_frame()
        draw_character_and_pass_it_to_next_frame_2()

        draw_health_bar(ryu.get_hp_ratio(), 20, 20)
        draw_health_bar(guile.get_hp_ratio(), 580, 20)
        guile.move(window.get_window())
        ryu.move(window.get_window())

        guile.draw(window.get_window())
        ryu.draw(window.get_window())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # to have better fps adjustment for bg map
        # if clock.get_time() % 2 == 0 :
        # map display

        # end map display
        """
        # guile display
        rect_guile = guile_anim[currentGuileFrame].get_rect().move(guile.position, 240)
        window.blit(guile_anim[currentGuileFrame], rect_guile)
        currentGuileFrame = (currentGuileFrame + 1) % len(guile_anim)

        rect_ryu = ryu_anim[currentRyuFrame].get_rect().move(ryu.position, 240)
        window.blit(ryu_anim[currentRyuFrame], rect_ryu)
        currentRyuFrame = (currentRyuFrame + 1) % len(ryu_anim)
 """
        # end guile display
        # get inputs
        """
        keys = pygame.key.get_pressed()
        if animating == 1:
            if guile_anim[0] == guile_anim[currentGuileFrame]:
                completedAnim = True
            if completedAnim:
                animating = 0
                guile.changeAnimation('idle', 'right')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
                completedAnim = False
            count += 1

        if animating != 1:
            if keys[K_q] and countKeyPressed(pygame.key.get_pressed()) <= 1:
                if guile.current_animation != 'back' or (guile.current_direction != ("right" if guile.position < 500 else "left")):
                    guile.changeAnimation('back', "right" if guile.position < 500 else "left")
                    guile_anim = loadGIF(guile.current_animation_path)
                    currentGuileFrame = 0
                guile.move(-20, guile_anim[0].get_width())
            elif keys[K_d] and countKeyPressed(pygame.key.get_pressed()) <= 1:
                if guile.current_animation != 'forward' or (guile.current_direction != ("right" if guile.position < 500 else "left")):
                    guile.changeAnimation('forward', "right" if guile.position < 500 else "left")
                    guile_anim = loadGIF(guile.current_animation_path)
                    currentGuileFrame = 0
                guile.move(+20, guile_anim[0].get_width())
            elif keys[K_e]:
                animating = 1
                guile.changeAnimation('long', "right" if guile.position < 500 else "left")
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            elif keys[K_SPACE]:
                animating = 1
                guile.changeAnimation('kick', "right" if guile.position < 500 else "left")
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            elif keys[K_f]:
                animating = 1
                guile.changeAnimation('punch', "right" if guile.position < 500 else "left")
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            elif keys[K_a]:
                animating = 1
                guile.changeAnimation('block', "right" if guile.position < 500 else "left")
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            else:
                if guile.current_animation != 'idle':
                    guile.changeAnimation('idle', "right" if guile.position < 500 else "left")
                    guile_anim = loadGIF(guile.current_animation_path)
                    currentGuileFrame = 0
 """
        pygame.display.flip()
        # end get inputs
