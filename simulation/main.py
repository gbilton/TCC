from typing import Dict
from uuid import UUID

import pygame

from simulation.environment import Environment
from simulation.levels import Level2


def main():
    level = Level2
    env = Environment(level)
    run = True
    vehicles, intersections = env.reset(level=level)
    timestep = 0
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
    main()
