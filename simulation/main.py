from typing import Callable, Dict
from uuid import UUID

import pygame

from simulation.environment import Environment
from simulation.intersection import Intersection
from simulation.levels import Level1, Level2


def main(num_vehicles, level, method: str):
    pygame.init()
    if not level:
        level = Level2
    env = Environment(level)
    if not num_vehicles:
        env.num_vehicles = num_vehicles
    env.render = False
    run = True
    vehicles, intersections = env.reset(level=level)
    timestep = 0

    if method == "act":
        for intersection in intersections:
            intersection.load_model("simulation/ai/models/model.tar")
            intersection.policy_net.eval()
            K = 60

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
            intersection.id: intersection.method(method, vehicles) for intersection in intersections
        }

        if method == "act":
            for _ in range(K):
                _, _, done = env.step(actions)
                if env.render:
                    env.draw_window()
                    env.clock.tick(env.FPS)
                for key, value in actions.items():
                    actions[key] = 0
                if done:
                    break
        else:
            _, _, done = env.step(actions)

        if done:
            # print("timestep: ", timestep)
            run = False

    # pygame.quit()

    # print(f"Time average = {env.timer/(env.num_vehicles*len(env.paths)*env.FPS):.2f}s")
    return env.timer / (env.num_vehicles * len(env.paths) * env.FPS)


if __name__ == "__main__":
    main(5, Level1, "act")
    main(5, Level1, "act")

    main(5, Level1, "formal_action")
    main(5, Level1, "formal_action")

    main(5, Level1, "random_action")
    main(5, Level1, "random_action")
