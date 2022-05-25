import pickle

import pygame
from results.episode import episode
from tqdm import tqdm
from simulation.levels import Level1, Level2

methods = ["random_action", "formal_action", "select_action"]
levels = [Level1, Level2]
number_cars = list(range(5, 10 + 1, 5))
# number_cars = [1]
iterations = 3

results = []
for method in tqdm(methods):
    for level in levels:
        for n in number_cars:
            for _ in tqdm(range(iterations)):
                score = episode(n, level, method)
                result = {
                    "number of cars": n,
                    "method": method,
                    "level": level.__name__,
                    "score": score,
                }
                results.append(result)

pygame.quit()

with open("results/results", "wb") as f:
    pickle.dump(results, f)
