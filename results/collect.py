import pickle

import pygame
from results.episode import episode
from tqdm import tqdm
from simulation.levels import Level1, Level2
from simulation.main import main

methods = ["random_action", "formal_action", "act"]
levels = [Level1, Level2]
number_cars = list(range(5, 30 + 1, 1))
# number_cars = [1]
iterations = 5
results = []

with tqdm(total=len(methods) * len(levels) * len(number_cars) * iterations) as pbar:
    for method in methods:
        for level in levels:
            for n in number_cars:
                for _ in range(iterations):
                    score = main(n, level, method)
                    result = {
                        "number of cars": n,
                        "method": method,
                        "level": level.__name__,
                        "score": score,
                    }
                    results.append(result)
                    pbar.update()

pygame.quit()

with open("results/results", "wb") as f:
    pickle.dump(results, f)
