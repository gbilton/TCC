from typing import Dict
from uuid import UUID
import pygame
from simulation.environment import Environment
from simulation.intersection import Intersection
from simulation.levels import Level1


def episode(num_vehicles, level, method):
    env = Environment(level)
    env.num_vehicles = num_vehicles
    env.render = False
    run = True
    vehicles, intersections = env.reset(level=level)
    timestep = 0

    for intersection in intersections:
        intersection.load_model("simulation/ai/models/model.tar")
        intersection.policy_net.eval()

    while run:
        timestep += 1

        if env.render:
            env.draw_window()
            env.clock.tick(env.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        actions: Dict[UUID, int] = {
            intersection.id: intersection.method(method, vehicles) for intersection in intersections
        }
        _, _, done = env.step(actions)

        if done:
            run = False

    # pygame.quit()

    return env.timer / (env.num_vehicles * len(env.paths) * env.FPS)


if __name__ == "__main__":
    episode(5, Level1, "select_action")
