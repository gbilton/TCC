import os
from typing import List

import pygame
from pygame.surface import Surface
from light import TrafficLight
from utils import TrafficLightState

from vehicle import Vehicle


WIDTH, HEIGHT = 900, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Semáforo Autônomo")
render = True
WHITE = (255, 255, 255)
FPS = 60

# image = pygame.image.load(os.path.join('sample', 'image'))

def initialize():
    start_point = (50, 50)
    end_point = (100, 100)
    MAX_SPEED = 4
    ACCELERATION = 1
    car = Vehicle(start_point, end_point, MAX_SPEED, ACCELERATION)
    light = TrafficLight((200, 200), TrafficLightState.green)
    cars = [car]
    lights = [light]
    return cars, lights


def draw_window(win: Surface, vehicles: List[Vehicle], lights: List[TrafficLight]):
    win.fill(WHITE)

    for vehicle in vehicles:
        vehicle.draw(win, (0, 116, 204))
        vehicle.draw_path(win)

    for light in lights:
        light.draw(win)

    pygame.display.update()


def step(vehicles: List[Vehicle], lights: List[TrafficLight]):
    for vehicle in vehicles:
        vehicle.move()
        vehicle.timer += 1
    
    for light in lights:
        if vehicles[0].timer % 100 == 0:
            light.change_state()


def main():
    vehicles, lights = initialize()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONUP:
                vehicles[0].add_point(event.pos)

        step(vehicles, lights)

        if render:
            draw_window(win, vehicles, lights)

    pygame.quit()


if __name__ == "__main__":
    main()