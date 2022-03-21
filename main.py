import pygame

from environment import Environment


def main():
    env = Environment()
    vehicles, lights = env.initialize()
    run = True
    while run:
        env.clock.tick(env.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                vehicles[0].add_point(event.pos)

        env.step(vehicles, lights)

        if env.render:
            env.draw_window(env.win, vehicles, lights)

    pygame.quit()


if __name__ == "__main__":
    main()