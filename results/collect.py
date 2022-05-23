import pickle

import pygame
from results.episode import episode
from tqdm import tqdm
from simulation.levels import Level1, Level2

methods = ["random_action", "formal_action", "select_action"]
levels = [Level1, Level2]
# number_cars = list(range(5, 31, 5))
number_cars = [1]
iterations = 1

results = []
for method in tqdm(methods):
    for level in levels:
        for n in number_cars:
            for _ in range(iterations):
                avg_time = episode(n, level, method)
                result = {
                    "number of cars": n,
                    "method": method,
                    "level": level.__name__,
                }
                results.append(result)
                print(":)")

pygame.quit()

with open("results/results", "wb") as f:
    pickle.dump(results, f)
