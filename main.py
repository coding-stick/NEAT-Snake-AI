import pygame, pickle, sys, neat
from pygame.locals import *
import pandas as pd
from Objects import Snake, Apple
from Objects import WIDTH, HEIGHT, SQUARE_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pygame Window')
pygame.init()
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

VISUALIZE_TRAINING = False # True -> training much SLOWER!! Set this to False and then load & see the winner file later.
FITNESS_DATA = [] # for analytics purposes


config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                    "config-feedforward.txt")

def get_inputs(snake, apple): # experiment with these, many unused functions in the Snake class 
    return [
        *snake.see_apple(apple),
        *snake.see_wall(),
        *snake.get_relative_pos(apple),
        *snake.get_dir(),
        *snake.see_local_body()
    ]


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        snake = Snake()
        apple = Apple()

        fitness = 0
        steps = 0
        running = True
        

        while running and steps < 1000:
            steps += 1
            # Get inputs for NN
            inputs = get_inputs(snake, apple)

            # Network decision
            output = net.activate(inputs)
            decision = output.index(max(output)) #0,1,2,3 : UDLR
            snake.turn_w_signal(decision)
            
            snake.move()

            # Check apple eating
            if snake.check_eat(apple):
                snake.length += 1
                snake.body.append(snake.body[-1])
                apple.random_position()
                fitness += 100
                steps = 0

            # encourage shorter games
            fitness -= 1

            # Check death
            if snake.check_collision():
                fitness -= 1000
                running = False

            if VISUALIZE_TRAINING and genome_id>20000:
                screen.fill((0, 0, 0))
                snake.draw(screen)
                apple.draw(screen)
                screen.blit(font.render(f'Score: {snake.length}', False, "white"), (0,0))
                screen.blit(font.render(f'Genome #: {genome_id}', False, "white"), (0,30))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                pygame.display.flip()
                clock.tick(100) # fps
            
        genome.fitness = fitness
        FITNESS_DATA.append(fitness)


def train(generations, filename, analytics = True):
    p = neat.Population(config)
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.StdOutReporter(True))

    winner = p.run(eval_genomes, generations) # generations

    if analytics:
        gen = list(range(len(stats.most_fit_genomes)))
        best = [c.fitness for c in stats.most_fit_genomes]
        avg = stats.get_fitness_mean()
        stdev = stats.get_fitness_stdev()

        df = pd.DataFrame({
            "generation": gen,
            "best_fitness": best,
            "avg_fitness": avg,
            "stdev": stdev
        })

        df.to_csv("fitness_log.csv", index=False)

    # Save winner to file
    with open(filename, "wb") as f:
        pickle.dump(winner, f)

    print("Winner saved to winner.pkl")


def load_play(filename):
    with open(filename, "rb") as f:
        winner = pickle.load(f)

    # Rebuild network from genome
    net = neat.nn.FeedForwardNetwork.create(winner, config)

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        inputs = get_inputs(snake, apple)
        
        output = net.activate(inputs)
        decision = output.index(max(output)) 
        print(output)
        snake.turn_w_signal(decision)
        snake.move()

        if snake.check_eat(apple):
            snake.length += 1
            snake.body.append(snake.body[-1])
            apple.random_position()

        if snake.check_collision():
            running = False

        # draw stuff
        
        screen.fill((0, 0, 0))
        snake.draw(screen)
        apple.draw(screen)
        screen.blit(font.render(f'Score: {snake.length}', False, "white"), (10,0))

        # draw grid (optional)
        for x in range(0, WIDTH, SQUARE_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, SQUARE_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(200)

    print("Replay finished, score:", snake.length - 1)



# ------------------DO STUFF HERE ----------------

train(200, "winner.pkl") # ---> winner.pkl, must run > 200 generations for effective results.

#load_play("winner.pkl")