import pygame
import random

BLUE = (0, 0, 255)


class Food:
    def __init__(self):
        self.size = 25
        self.x = random.randint(0, 600 - self.size)
        self.y = random.randint(0, 600 - self.size)
        self.color = BLUE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))
