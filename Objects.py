import pygame
from pygame.locals import *
import random


WIDTH = 800
HEIGHT = 600
SQUARE_SIZE = 20

class Snake:
    def __init__(self, starting_pos = (WIDTH/2, HEIGHT/2), starting_length = 2):
        self.body = []
        for i in range(starting_length):
            x = starting_pos[0] - i * SQUARE_SIZE
            y = starting_pos[1]
            if i == 0:
                self.body = [(x, y)]
            else:
                self.body.append((x, y))
        self.length = starting_length
        self.direction = (SQUARE_SIZE, 0)  # Moving right initially

        self.head = self.body[0]

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()  # Remove the tail segment

        self.head = (self.body[0])

    def decode_direction(self, new_dir):
        # UDLR
        if new_dir == 0:
            return (0, -SQUARE_SIZE)
        elif new_dir == 1: 
            return (0, SQUARE_SIZE)
        elif new_dir == 2: 
            return (-SQUARE_SIZE, 0)
        elif new_dir == 3:
            return (SQUARE_SIZE, 0)
    
    def turn_w_signal(self, new_direction):
        self.direction = self.decode_direction(new_direction)
        self.head = (self.body[0])

    def turn(self, new_direction):
        if (new_direction[0] != 0 and self.direction[0] == 0) or (new_direction[1] != 0 and self.direction[1] == 0):
            self.direction = new_direction
        self.head = (self.body[0])
    
    def draw(self, surface):
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(segment[0], segment[1], SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, (255, 255, 255) if i == 0 else (0, 255, 0), rect)

    def see_apple(self, apple):
        up = (0, -SQUARE_SIZE)
        down = (0, SQUARE_SIZE)
        left = (-SQUARE_SIZE, 0)
        right = (SQUARE_SIZE, 0)

        directions = [up, down, left, right]
        apple_present = [0,0,0, 0]

        for i, d in enumerate(directions):
            x, y = self.head[0], self.head[1]
            while True:
                x += d[0]
                y += d[1]

                #hit wall
                if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                    break
                if (x, y) == apple.position:
                    apple_present[i] = 1
                    break
        return tuple(apple_present)
    
    def get_relative_pos(self, apple):
        return ((self.head[0]-apple.position[0])/WIDTH, (self.head[1]-apple.position[1])/HEIGHT)

    def see_body(self):
        up = (0, -SQUARE_SIZE)
        down = (0, SQUARE_SIZE)
        left = (-SQUARE_SIZE, 0)
        right = (SQUARE_SIZE, 0)

        directions = [up, down, left, right]
        dangers = []

        for i, d in enumerate(directions):
            x, y = self.head[0], self.head[1]
            dist = 0
            while True:
                dist += SQUARE_SIZE
                x += d[0]
                y += d[1]

                #hit snake
                if (x, y) in self.body[1:] or x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                    break
            # change these to be divided by SQUARE_SIZE (optional)
            if i==0 or i==1:
                dangers.append(dist/SQUARE_SIZE)
            else:
                dangers.append(dist/SQUARE_SIZE)
        return tuple(dangers)
    
    def see_local_body(self, n=1):
        head_x, head_y = self.head
        
        local_body = []
        for dy in range(-SQUARE_SIZE*n, SQUARE_SIZE*(n+1), SQUARE_SIZE):
            for dx in range(-SQUARE_SIZE*n, SQUARE_SIZE*(n+1), SQUARE_SIZE):
                if dx == 0 and dy == 0:  # Skip head position
                    continue
                
                check_pos = (head_x + dx, head_y + dy)

                if check_pos in self.body[1:]:
                    local_body.append(1)
                else:
                    local_body.append(0)
        
        return local_body 

    
    def see_wall(self):
        return tuple([self.head[1]/HEIGHT, (HEIGHT - self.head[1])/HEIGHT, self.head[0]/WIDTH, (WIDTH-self.head[0])/WIDTH])

    def check_eat(self, apple):
        return self.head== apple.position
    def check_collision(self):
        return (self.head in self.body[1:]) or (self.head[0] < 0 or self.head[0] >= WIDTH or self.head[1] < 0 or self.head[1] >= HEIGHT)
   

    def one_hot_tail_dir(self):
        # Map direction tuples to one-hot vectors
        direction_map = {
            (0, -SQUARE_SIZE): [0, 1, 0, 0],  # Up
            (0, SQUARE_SIZE):  [1, 0, 0, 0],  # Down  
            (-SQUARE_SIZE, 0): [0, 0, 0, 1],  # Left
            (SQUARE_SIZE, 0):  [0, 0, 1, 0],  # Right
        }
        
        return direction_map.get(self.direction, [0, 0, 0, 0])
    
    def get_dir(self):
        return (self.direction[0]/SQUARE_SIZE, self.direction[1]/SQUARE_SIZE)

class Apple:
    def __init__(self):
        self.random_position()

    def draw(self, surface):
        rect = pygame.Rect(self.position[0], self.position[1], SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(surface, (255, 0, 0), rect)

    def random_position(self):
        self.position = (random.randint(0, (WIDTH - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE,
                         random.randint(0, (HEIGHT - SQUARE_SIZE) // SQUARE_SIZE) * SQUARE_SIZE)