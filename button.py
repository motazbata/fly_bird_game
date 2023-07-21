import pygame
from pygame.locals import *

screen_width = 640
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        # Check if space key is pressed
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            action = True

        # Draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action
