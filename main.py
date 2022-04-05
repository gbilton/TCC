import pygame

from environment import Environment
from level1 import Level1


def main():
    env = Environment()
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

        done = env.step(vehicles, lights)

        if done:
            run = False


    pygame.quit()


if __name__ == "__main__":
    main()