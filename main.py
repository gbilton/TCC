import os

import pygame

from vehicle import Vehicle


WIDTH, HEIGHT = 900, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Semáforo Autônomo")

WHITE = (255, 255, 255)
FPS = 60

# image = pygame.image.load(os.path.join('sample', 'image'))

def initialize():
    start_point = (50, 50)
    end_point = (100, 100)
    MAX_SPEED = 4
    ACCELERATION = 1
    car = Vehicle(start_point, end_point, MAX_SPEED, ACCELERATION)
    return car


def draw_window(car):
    win.fill(WHITE)
    car.draw(win, (0, 116, 204))
    car.draw_path(win)
    # win.blit(image, (location))
    pygame.display.update()


def main():
    car = initialize()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                car.add_point(event.pos)
        car.move()
        car.timer += 1
        draw_window(car)
    pygame.quit()


if __name__ == "__main__":
    main()