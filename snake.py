import pygame
from cell import Cell

GREEN = (0, 255, 0)


"""
If the snake eats food then don't pop the last element
"""


class Snake:
    def __init__(self):
        self.color = GREEN
        self.body = 30
        self.velocity = 30
        self.direction = [0, 0]
        self.eating_stage = False
        self.container = [Cell(300, 500)]

    def move(self):
        """
        Use the direction attribute to navigate path
        """
        self.container.insert(
            0,
            Cell(
                self.container[0].x + self.direction[0] * self.velocity,
                self.container[0].y + self.direction[1] * self.velocity,
            ),
        )
        if self.eating_stage:
            self.eating_stage = False
        else:
            self.container.pop()

        # if self.container[0].x + self.body < 0:
        #     self.container[0].x = 600
        # if self.container[0].x > 600:
        #     self.container[0].x = 0
        # if self.container[0].y + self.body < 0:
        #     self.container[0].y = 600
        # if self.container[0].y > 600:
        #     self.container[0].y = 0

    def draw(self, window):
        for cell in self.container:
            pygame.draw.rect(window, (0, 0, 0), (cell.x, cell.y, self.body, self.body))
            pygame.draw.rect(
                window,
                self.color,
                (cell.x + 5, cell.y + 5, self.body - 10, self.body - 10),
            )
