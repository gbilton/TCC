import pygame

from environment import Environment
from level1 import Level1


def main():
    env = Environment(Level1)
    level = Level1
    vehicles, lights = env.initialize(level=level)
    run = True
    while run:
        if env.render:
            env.draw_window()
            env.clock.tick(env.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                vehicles[0].add_point(event.pos)
                print(event.pos)

        done = env.step(vehicles, lights)

        if done:
            run = False


    pygame.quit()

    print(f"Time average = {env.timer/(env.num_vehicles*len(env.paths)*env.FPS):.2f}s")

if __name__ == "__main__":
    main()