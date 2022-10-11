import pygame as pygame
from pygame import *

from libraries.characters import Guile
from libraries.music import *
from libraries.gifLoader import *

if __name__ == "__main__":
    # initialize game and window
    pygame.init()

    window = pygame.display.set_mode((1000, 440))
    clock = pygame.time.Clock()
    mapFrameList = loadGIF("assets/map/air-force-base.gif")
    guile = Guile()
    currentFrame = 0
    currentGuileFrame = 0
    run = True
    loadLoadAndPlayBGM("assets/audio/map-stages/air-force-base.mp3")
    print(guile.current_animation_path)
    guile_anim = loadGIF(guile.current_animation_path)

    while run:

        clock.tick(14)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill(0)
        # to have better fps adjustment for bg map
        # if clock.get_time() % 2 == 0 :
        # map display
        rect = mapFrameList[currentFrame].get_rect()
        window.blit(mapFrameList[currentFrame], rect)
        currentFrame = (currentFrame + 1) % len(mapFrameList)
        # end map display

        # guile display
        rect_guile = guile_anim[currentGuileFrame].get_rect().move(guile.position, 240)

        window.blit(guile_anim[currentGuileFrame], rect_guile)
        currentGuileFrame = (currentGuileFrame + 1) % len(guile_anim)

        # end guile display
        pygame.display.flip()

        # get inputs

        keys = pygame.key.get_pressed()
        if keys[K_q]:
            if guile.current_animation != 'left_idle':
                guile.changeAnimation('left_idle')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0

            print("left")
        if keys[K_d]:
            if guile.current_animation != 'right_idle':
                guile.changeAnimation('right_idle')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0

            print("right")

        # end get inputs
