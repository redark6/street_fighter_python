import pygame


class Window:
    def __init__(self, map):
        self.map = map
        self.window = pygame.display.set_mode((map.WIDTH, map.HEIGHT))
        pygame.display.set_caption("Street Fighter")

    def fill(self, fill_value):
        self.window.fill(fill_value)

    def blit(self, frame, rect):
        self.window.blit(frame, rect)

    def get_window(self):
        return self.window
