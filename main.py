import pygame
from snake import Snake
from food import Food

WIDTH, HEIGHT = 600, 600


def render_graphics(window, snake, food):
    window.fill((0, 0, 0))
    snake.draw(window)
    food.draw(window)
    pygame.display.update()


def collision_detection(snake, food):
    food_object = pygame.Rect(food.x, food.y, food.size, food.size)
    for cell in snake.container:
        cell_object = pygame.Rect(cell.x, cell.y, snake.body, snake.body)
        if cell_object.colliderect(food_object):
            return True
    return False


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake AI")
    snake = Snake()
    food = Food()
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.direction != [1, 0]:
                    snake.direction = [-1, 0]
                if event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
                    snake.direction = [1, 0]
                if event.key == pygame.K_DOWN and snake.direction != [0, -1]:
                    snake.direction = [0, 1]
                if event.key == pygame.K_UP and snake.direction != [0, 1]:
                    snake.direction = [0, -1]
        snake.move()
        """ Check for collision """
        if collision_detection(snake, food):
            food = Food()
            snake.eating_stage = True
        render_graphics(window, snake, food)
        clock.tick(20)


main()