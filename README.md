# Snake AI with NEAT

This project uses NeuroEvolution of Augmenting Topologies (NEAT) to train an AI agent to play the classic Snake game. The snake learns over generations through evolutionary strategies to avoid collisions, collect apples, and maximize its score.

## Features

Snake game built with Pygame.

AI controlled by Python-NEAT neural networks.

Fitness function rewards longer survival and apple collection.

Training progress saved to .pkl file for later visualization.

Fitness scores can be logged for analytics and graphing.

## Installation

In your command line, 

``` bash
pip install pygame neat-python pandas
```

## Usage

Scroll to the end of main.py and change the code to your liking

Run training for a set number of generations:

(If you want to try playing the game yourself first, run game_only.py)

This will run evolution using NEAT.

The best genome of the run will be saved as winner.pkl.

Then run 




This opens a Pygame window showing the snake playing using the trained neural net.

3. Analyze Fitness Data

If you enabled logging fitness scores to a .csv file, you can open analysis.ipynb to visualize generation performance graphs.
