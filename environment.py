from tokenize import Triple
from typing import Dict, List, Tuple
import pygame
from pygame.surface import Surface
from level1 import Level

from vehicle import Vehicle
from light import TrafficLight
from utils import TrafficLightState


class Environment:
    pygame.display.set_caption("Semáforo Autônomo")

    WIDTH, HEIGHT = 900, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    
    clock = pygame.time.Clock()
    render: bool = True
    FPS: int = 60

    vehicles: List[Vehicle] = []
    lights: List[TrafficLight] = []
    paths: Dict[str, List[Tuple[int, int]]]


    def initialize(self, level):
        self.paths = level.paths

        car2_path = [(50,50)]
        car2_path += (self.paths["a"])
        MAX_SPEED = level.MAX_SPEED
        
        car = Vehicle(path_code="a", path=self.paths["a"], MAX_SPEED=1)
        car2 = Vehicle(path_code="a", path=car2_path, MAX_SPEED=2)
        # car2 = Vehicle(path_code="b", path=self.paths["b"], MAX_SPEED=MAX_SPEED)
        light = TrafficLight((200, 200), TrafficLightState.green)
        
        self.vehicles.append(car)
        self.vehicles.append(car2)
        self.lights.append(light)

        return self.vehicles, self.lights


    def draw_window(self):
        WHITE = (255, 255, 255)
        self.win.fill(WHITE)

        for vehicle in self.vehicles:
            vehicle.draw(self.win, (0, 116, 204))
            vehicle.draw_path(self.win)

        for light in self.lights:
            light.draw(self.win)

        pygame.display.update()


    def step(self, vehicles: List[Vehicle], lights: List[TrafficLight]):
        for vehicle in vehicles:
            other_vehicles = vehicles[:]
            other_vehicles.remove(vehicle)
            vehicle.move(other_vehicles)
            vehicle.timer += 1

        for light in lights:
            if vehicles[0].timer % 100 == 0:
                light.change_state()
