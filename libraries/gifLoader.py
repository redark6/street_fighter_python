import pygame
from PIL import Image, ImageSequence


def pilImageToSurface(pilImage):
    mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


def loadGIF(filename):
    pil_image = Image.open(filename)
    frames = []
    if pil_image.format == 'GIF' and pil_image.is_animated:
        for frame in ImageSequence.Iterator(pil_image):
            pygame_image = pilImageToSurface(frame.convert('RGBA'))
            frames.append(pygame_image)
    else:
        frames.append(pilImageToSurface(pil_image))
    return frames
