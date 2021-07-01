import pygame
from snake import Snake
from food import Food
from ai_agent import Agent

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("your_font.ttf", 25)

WIDTH, HEIGHT = 600, 600


def render_graphics(window, snake, food, score, best_score):
    window.fill((25, 25, 25))
    pygame.draw.rect(window, (0, 0, 0), (0, 590, WIDTH, 10))
    snake.draw(window)
    food.draw(window)
    SCORE = font.render(f"SCORE: {score}", False, (255, 255, 255))
    window.blit(SCORE, (WIDTH - 3 * (WIDTH // 20), 0))
    BEST_SCORE = font.render(f"BEST SCORE: {best_score}", False, (255, 255, 255))
    window.blit(BEST_SCORE, (0, 0))
    pygame.display.update()


def food_consumption(snake, food):
    food_object = pygame.Rect(
        food.x - food.size // 2, food.y - food.size // 2, food.size, food.size
    )
    head_object = pygame.Rect(
        snake.container[0].x, snake.container[0].y, snake.body, snake.body
    )
    if head_object.colliderect(food_object):
        return True
    return False


def check_collision(snake):
    head = snake.container[0]
    if (
        head.x + 10 < 0
        or head.x + snake.body - 10 > WIDTH
        or head.y + 10 < 0
        or head.y + snake.body - 10 > WIDTH
    ):
        return True
    head_object = pygame.Rect(
        head.x,
        head.y,
        snake.body,
        snake.body,
    )
    for i in range(1, len(snake.container)):
        body = pygame.Rect(
            snake.container[i].x,
            snake.container[i].y,
            snake.body,
            snake.body,
        )
        if head_object.colliderect(body):
            return True
    return False


def main(best_score):
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake AI")
    snake = Snake()
    food = Food(snake)
    score = 0
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT and snake.direction != [1, 0]:
            #         snake.direction = [-1, 0]
            #     if event.key == pygame.K_RIGHT and snake.direction != [-1, 0]:
            #         snake.direction = [1, 0]
            #     if event.key == pygame.K_DOWN and snake.direction != [0, -1]:
            #         snake.direction = [0, 1]
            #     if event.key == pygame.K_UP and snake.direction != [0, 1]:
            #         snake.direction = [0, -1]
        """
        AI agent will make decision here(Change it's direction or keep it as it is)
        """
        Agent.makeDecision(snake, food)
        snake.move()
        """ Check for collision """
        if food_consumption(snake, food):
            food = Food(snake)
            snake.eating_stage = True
            score += 1
        if check_collision(snake):
            best_score = max(score, best_score)
            main(best_score)
            # run = False
            # pygame.quit()
        render_graphics(window, snake, food, score, best_score)
        clock.tick(30)


if __name__ == "__main__":
    best_score = 0
    main(best_score)
