import pygame
from PIL import Image, ImageSequence


def pil_image_to_surface(pilImage):
    mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
    return pygame.image.fromstring(data, size, mode).convert_alpha()


def load_gif(filename):
    pil_image = Image.open(filename)
    frames = []
    if pil_image.format == 'GIF' and pil_image.is_animated:
        for frame in ImageSequence.Iterator(pil_image):
            pygame_image = pil_image_to_surface(frame.convert('RGBA'))
            frames.append(pygame_image)
    else:
        frames.append(pil_image_to_surface(pil_image))
    return frames
