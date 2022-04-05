import math
from typing import Dict, List, Tuple
import random

import pygame

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

    timer: float = 0


    def calculate_start_point(self, point, path: List[Tuple[int, int]]):
        start_x, start_y = path[0]
        target_x, target_y = path[1]

        x_diff = target_x - start_x
        y_diff = target_y - start_y

        if y_diff == 0:
            y_diff = -0.01
            # desired_radian_angle = math.pi / 2
        
        desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > start_y:
            desired_radian_angle += math.pi

        angle = math.degrees(desired_radian_angle+math.pi)
        start_point = (start_x - math.sin(math.radians(angle)) *
                       point, start_y - math.cos(math.radians(angle)) * point)
        return start_point

    def initialize(self, level):
        self.paths = level.paths

        for key, value in self.paths.items():
            path_code = key
            path = value

            # num_vehicles = random.randrange(1, 10, 1)
            num_vehicles = 10
            points = [i*random.normalvariate(50, 5) for i in range(1, num_vehicles+1)]

            for i in range(num_vehicles):

                start_point = [self.calculate_start_point(points[i], path)]
                vehicle_path = start_point + path

                vehicle = Vehicle(path_code=path_code, path=vehicle_path, MAX_SPEED=level.MAX_SPEED)
                self.vehicles.append(vehicle)

        light = TrafficLight((200, 250), TrafficLightState.green)
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
            if vehicle.complete_path:
                self.timer += vehicle.total_time
                vehicles.remove(vehicle)
                continue
            other_vehicles = vehicles[:]
            other_vehicles.remove(vehicle)
            vehicle.move(other_vehicles, lights)
            vehicle.timer += 1

        for light in lights:
            if vehicles[0].timer % 200 == 0:
                light.change_state()
