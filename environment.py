from typing import List
import pygame
from pygame.surface import Surface

from vehicle import Vehicle
from light import TrafficLight
from utils import TrafficLightState


class Environment:
    WIDTH, HEIGHT = 900, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Semáforo Autônomo")
    clock = pygame.time.Clock()
    render = True
    FPS = 60
    WHITE = (255, 255, 255)


    def initialize(self):
        start_point = (50, 50)
        end_point = (100, 100)
        MAX_SPEED = 4
        ACCELERATION = 1
        car = Vehicle(start_point, end_point, MAX_SPEED, ACCELERATION)
        light = TrafficLight((200, 200), TrafficLightState.green)
        cars = [car]
        lights = [light]
        return cars, lights


    def draw_window(self, win: Surface, vehicles: List[Vehicle], lights: List[TrafficLight]):
        win.fill(self.WHITE)

        for vehicle in vehicles:
            vehicle.draw(win, (0, 116, 204))
            vehicle.draw_path(win)

        for light in lights:
            light.draw(win)

        pygame.display.update()


    def step(self, vehicles: List[Vehicle], lights: List[TrafficLight]):
        for vehicle in vehicles:
            vehicle.move()
            vehicle.timer += 1

        for light in lights:
            if vehicles[0].timer % 100 == 0:
                light.change_state()
