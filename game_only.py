import pygame, random
from pygame.locals import *

from Objects import Snake, Apple
from Objects import WIDTH, HEIGHT, SQUARE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()


font = pygame.font.Font(None, 36)



apple = Apple()

snake = Snake(starting_length=20)




clock = pygame.time.Clock()

running = True
while running:
    # !! THIS BEFORE EVERYTHING ELSE
    if snake.check_collision():
        print("Game Over")
        running = False
    
    screen.fill((0, 0, 0))

    # draw grid (optional)
    for x in range(0, WIDTH, SQUARE_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, SQUARE_SIZE):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

    # draw snake
    snake.draw(screen)
    apple.draw(screen)

    #print('Wall: ', snake.see_wall(), 'Body: ', snake.see_body(), 'Apple: ', snake.see_apple(apple), 'Dir:', tuple(d/SQUARE_SIZE for d in snake.direction))
    
    
    if snake.check_eat(apple):
        snake.length += 1
        snake.body.append(snake.body[-1])
        apple.random_position()


    snake.move()

    
    screen.blit(font.render(f'Score: {snake.length}', True, (255, 255, 255)), (10, 10))



    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP:
                snake.turn_w_signal(0)
                #snake.turn((0, -SQUARE_SIZE))
            elif event.key == K_DOWN:
                snake.turn_w_signal(1)
                #snake.turn((0, SQUARE_SIZE))
            elif event.key == K_LEFT:
                snake.turn_w_signal(2)
                #snake.turn((-SQUARE_SIZE, 0))
            elif event.key == K_RIGHT:
                snake.turn_w_signal(3)
                #snake.turn((SQUARE_SIZE, 0))

    pygame.display.flip()
    clock.tick(30)
pygame.quit()
