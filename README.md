# Snake AI with NEAT

This project uses NeuroEvolution of Augmenting Topologies (NEAT) to train an AI agent to play the classic Snake game. The snake learns over generations through evolutionary strategies to avoid collisions, collect apples, and maximize its score.

<img width="941" height="722" alt="Screenshot 2025-08-26 191501" src="https://github.com/user-attachments/assets/a395925e-3902-4a32-aec2-7fa4d38f2a4b" />

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

Run training() for a set number of generations

(If you want to try playing the game yourself first, run game_only.py)

This will run evolution using NEAT.

The best genome of the run will be saved as winner.pkl.

Then run load_play()

This opens a Pygame window showing the snake playing using the trained neural net.

If you enabled logging fitness scores to a .csv file, you can open analysis.ipynb to visualize generation performance graphs.

<img width="1839" height="926" alt="output" src="https://github.com/user-attachments/assets/9dd18ca7-26e5-4900-848b-c4ee83490498" />


