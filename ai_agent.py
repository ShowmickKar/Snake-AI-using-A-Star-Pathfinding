import pygame
import math
import random
from queue import PriorityQueue


class Agent:
    DIRECTIONS = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    current_path = []

    @staticmethod
    def manhattenDistance(snake_position, food_position):
        return abs(snake_position[0] - food_position[0]) + abs(
            snake_position[1] - food_position[1]
        )

    @staticmethod
    def reconstructPath(came_from, current):
        """
        Will return an array containing the optimal path
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        print(f"path: {path}")
        return path

    @staticmethod
    def getNeighbors(snake, current):
        neighbors = [
            (
                current[0] + snake.velocity * Agent.DIRECTIONS[i][0],
                current[0] + snake.velocity * Agent.DIRECTIONS[i][1],
            )
            for i in range(4)
        ]
        for neighbor in neighbors:
            if (
                neighbor[0] < 0
                or neighbor[0] > 600
                or neighbor[1] < 0
                or neighbor[1] > 600
            ):
                neighbors.remove(neighbor)
            if Agent.collision(neighbor, snake):
                neighbors.remove(neighbor)
        return neighbors

    @staticmethod
    def reached(current, food):
        current_object = pygame.Rect(current[0], current[1], 30, 30)
        end_object = pygame.Rect(
            food.x - food.size // 2, food.y - food.size // 2, food.size, food.size
        )
        if current_object.colliderect(end_object):
            print(current_object, end_object)
            return True
        return False

    @staticmethod
    def aStar(snake, food):

        """ return the path from reconstruct_path method """

        start = snake.container[0].x, snake.container[0].y
        end = food.x, food.y
        count = 0
        priority_queue = PriorityQueue()
        priority_queue.put((0, count, start))
        came_from = {}
        g_score = {}
        g_score[start] = 0
        f_score = {}
        f_score[start] = Agent.manhattenDistance(start, end)
        open_set = {start}
        while not priority_queue.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = priority_queue.get()[2]
            open_set.remove(current)
            if Agent.reached(current, food):
                # print(f"Found{current, food}")
                return Agent.reconstructPath(came_from, current)
            neighbors = Agent.getNeighbors(snake, start)
            # print(current)
            for neighbor in neighbors:
                if neighbor not in g_score:
                    g_score[neighbor] = math.inf
                    f_score[neighbor] = math.inf
                tentative_g_score = g_score[current] + snake.velocity
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + Agent.manhattenDistance(
                        neighbor, end
                    )
                    if neighbor not in open_set:
                        count += 1
                        priority_queue.put((f_score[neighbor], count, neighbor))
                        open_set.add(neighbor)
        return []

    @staticmethod
    def collision(new_head_pos, snake):
        new_head_pos = pygame.Rect(
            new_head_pos[0], new_head_pos[1], snake.body, snake.body
        )
        for i in range(1, len(snake.container)):
            cell_object = pygame.Rect(
                snake.container[i].x, snake.container[i].y, snake.body, snake.body
            )
            if new_head_pos.colliderect(cell_object):
                return True
        return False

    @staticmethod
    def makeDecision(snake, food):

        """
        The purpose of the function is to calculate the optimal path using A* algorithm and set the snake's direction accordingly
        """
        head = snake.container[0]
        neighbors = [
            (
                head.x + snake.velocity * Agent.DIRECTIONS[i][0],
                head.y + snake.velocity * Agent.DIRECTIONS[i][1],
            )
            for i in range(4)
        ]

        try:
            if not len(Agent.current_path):
                Agent.current_path = Agent.aStar(snake, food)
            try:
                for i, neighbor in enumerate(neighbors):
                    if neighbor == Agent.current_path[-1]:
                        snake.direction = Agent.DIRECTIONS[i]
                        Agent.current_path.pop()
                        return
            except Exception as e:
                pass  # empty list
        except Exception as e:
            print(e)
            return
        if not len(Agent.current_path):
            direction = snake.direction
            distance = math.inf
            for i, path in enumerate(neighbors):
                if Agent.manhattenDistance(path, (food.x, food.y)) < distance:
                    """ Check for turn around attempts """

                    """ Check for the snake colliding with itself """

                    if Agent.collision(path, snake):
                        continue
                    direction = Agent.DIRECTIONS[i]
                    distance = Agent.manhattenDistance(path, (food.x, food.y))

            snake.direction = direction
