import pygame as pygame

from libraries.music import *
from libraries.gifLoader import *

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1000, 440))
    clock = pygame.time.Clock()

    gifFrameList = loadGIF("assets/map/air-force-base.gif")
    currentFrame = 0

    run = True
    loadLoadAndPlayBGM("assets/audio/map-stages/air-force-base.mp3")

    while run:

        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill(0)

        rect = gifFrameList[currentFrame].get_rect()
        window.blit(gifFrameList[currentFrame], rect)
        currentFrame = (currentFrame + 1) % len(gifFrameList)

        pygame.display.flip()
