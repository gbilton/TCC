from typing import Callable, Dict
from uuid import UUID

import pygame

from simulation.environment import Environment
from simulation.intersection import Intersection
from simulation.levels import Level1, Level2


def main(method: Callable):
    level = Level1
    env = Environment(level)
    env.render = False
    run = True
    vehicles, intersections = env.reset(level=level)
    timestep = 0

    # for intersection in intersections:
    #     intersection.load_model("simulation/ai/models/model.tar")
    #     intersection.policy_net.eval()

    while run:
        timestep += 1

        if env.render:
            env.draw_window()
            env.clock.tick(env.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                vehicles[0].add_point(event.pos)
                print(event.pos)

        actions: Dict[UUID, int] = {
            intersection.id: intersection.random_action(vehicles) for intersection in intersections
        }
        _, _, done = env.step(actions)

        if done:
            print("timestep: ", timestep)
            run = False

    pygame.quit()

    print(f"Time average = {env.timer/(env.num_vehicles*len(env.paths)*env.FPS):.2f}s")


if __name__ == "__main__":
    main(Intersection.random_action)
