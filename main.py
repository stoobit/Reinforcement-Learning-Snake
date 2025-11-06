# Packages
import random
import pygame
import sys

# Files
from direction import Direction
import colors as colors
import matrix as mtrx

pygame.init()
matrix = mtrx.generate(size=50)

# Sizes
field = 10
size = (len(matrix) * field, len(matrix) * field)
screen = pygame.display.set_mode(size)

# Other Settings
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Movements
turn_fields = []

# Game
fruit = None
gameOver = False

# Speed
snake_speed = 7  
frame_count = 0

# Snake
snake = [[10, 25, Direction.RIGHT]]
def isSnake(x, y):
    for part in snake:
        if part[0] == x and part[1] == y:
            return True
    
    return False

def inGame():
    return (snake[0][0] < len(matrix)) and (snake[0][1] < len(matrix)) and (snake[0][0] >= 0) and (snake[0][1] >= 0)

while gameOver == False:
    # Handle events so the window stays responsive
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP) and (snake[0][2] != Direction.DOWN):
                snake[0][2] = Direction.UP
            elif (event.key == pygame.K_DOWN) and (snake[0][2] != Direction.UP):
                snake[0][2] = Direction.DOWN
            elif (event.key == pygame.K_LEFT) and (snake[0][2] != Direction.RIGHT):
                snake[0][2] = Direction.LEFT
            elif (event.key == pygame.K_RIGHT) and (snake[0][2] != Direction.LEFT):
                snake[0][2] = Direction.RIGHT

            if len(snake) > 1:
                turn_fields.append((snake[0][0], snake[0][1], snake[0][2]))

    screen.fill(colors.WHITE)

    for x in range(len(matrix)):
        for y in range(len(matrix)):
            color = colors.RED if isSnake(x, y) else colors.GREEN
            pygame.draw.rect(screen, color, [
                x * field, y * field, field, field
            ],0)
    
    if fruit == None:
        bound = len(matrix) - 1

        x = random.randint(0, bound)
        y = random.randint(0, bound)
        fruit = (x, y)
    
    if (fruit[0] == snake[0][0]) and (fruit[1] == snake[0][1]): 
        last_segment = snake[-1]

        dx, dy = last_segment[2].value
        new_segment = [
            last_segment[0] - dx, 
            last_segment[1] - dy, 
            last_segment[2]
        ]

        snake.append(new_segment)
        fruit = None
    else:  
        pygame.draw.rect(screen, colors.BLUE, [
            fruit[0] * field, fruit[1] * field, field, field
        ],0)

    frame_count += 1
    if frame_count >= snake_speed:
        frame_count = 0

        turns_to_remove = []
        last_segment = snake[-1]
        for turn in turn_fields:
            if (turn[0] == last_segment[0]) and (turn[1] == last_segment[1]):
                turns_to_remove.append(turn)

        for segment in snake:
            rest = snake[:]
            rest.remove(segment)

            for item in rest:
                if (segment[0] == item[0]) and (segment[1] == item[1]):
                    gameOver = True

            for turn in turn_fields:
                if (turn[0] == segment[0]) and (turn[1] == segment[1]):
                    segment[2] = turn[2]

            dx, dy = segment[2].value
            segment[0] += dx
            segment[1] += dy

        for turn in turns_to_remove:
            turn_fields.remove(turn)


    if inGame() == False:
        gameOver = True

    pygame.display.flip()
    clock.tick(60)
