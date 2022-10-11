from pygame import *

from libraries.characters import Guile
from libraries.music import *
from libraries.gifLoader import *

def countKeyPressed(keys):
    return sum(x == True for x in keys)

if __name__ == "__main__":
    # initialize game and window
    pygame.init()

    window = pygame.display.set_mode((1000, 440))
    clock = pygame.time.Clock()
    mapFrameList = loadGIF("assets/map/air-force-base.gif")
    guile = Guile(1000)
    currentFrame = 0
    currentGuileFrame = 0
    run = True
    loadLoadAndPlayBGM("assets/audio/map-stages/air-force-base.mp3")
    guile_anim = loadGIF(guile.current_animation_path)

    animating = 0
    count = 0
    completedAnim = False

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
        # get inputs
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
                if guile.current_animation != 'back':
                    guile.changeAnimation('back', 'right')
                    guile_anim = loadGIF(guile.current_animation_path)
                    currentGuileFrame = 0
                guile.move(-20, guile_anim[0].get_width())
            elif keys[K_d] and countKeyPressed(pygame.key.get_pressed()) <= 1:
                if guile.current_animation != 'forward':
                    guile.changeAnimation('forward', 'right')
                    guile_anim = loadGIF(guile.current_animation_path)
                    currentGuileFrame = 0
                guile.move(+20, guile_anim[0].get_width())
            elif keys[K_e]:
                animating = 1
                guile.changeAnimation('long', 'right')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            elif keys[K_f]:
                animating = 1
                guile.changeAnimation('punch', 'right')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            elif keys[K_SPACE]:
                animating = 1
                guile.changeAnimation('kick', 'right')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            elif keys[K_f]:
                animating = 1
                guile.changeAnimation('punch', 'right')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            elif keys[K_a]:
                animating = 1
                guile.changeAnimation('block', 'right')
                guile_anim = loadGIF(guile.current_animation_path)
                currentGuileFrame = 0
            else:
                if guile.current_animation != 'idle':
                    guile.changeAnimation('idle', 'right')
                    guile_anim = loadGIF(guile.current_animation_path)
                    currentGuileFrame = 0

        pygame.display.flip()
        # end get inputs

