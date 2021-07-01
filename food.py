import pygame
import random

RED = (255, 0, 0)


class Food:
    def __init__(self, snake):
        self.size = 25
        self.x, self.y = self.place(snake)
        self.color = RED

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.size // 2, 0)

    def __collision(self, x, y, snake):
        food_object = pygame.Rect(
            x - self.size // 2, y - self.size // 2, self.size, self.size
        )
        for cell in snake.container:
            cell_object = pygame.Rect(cell.x, cell.y, snake.body, snake.body)
            if food_object.colliderect(cell_object):
                return True

        return False

    def place(self, snake):
        x = random.randint(self.size // 2, 600 - self.size // 2)
        y = random.randint(self.size // 2, 600 - self.size // 2)
        while self.__collision(x, y, snake):
            x = random.randint(self.size // 2, 600 - self.size // 2)
            y = random.randint(self.size // 2, 600 - self.size // 2 - 5)
        return x, y
