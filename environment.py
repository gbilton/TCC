import math
from typing import Dict, List, Tuple
import random

import pygame

from vehicle import Vehicle


class Environment:
    pygame.display.set_caption("Semáforo Autônomo")

    WIDTH, HEIGHT = 900, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    
    clock = pygame.time.Clock()
    render: bool = True
    FPS: int = 60

    vehicles: List[Vehicle] = []
    paths: Dict[str, List[Tuple[int, int]]]

    timer: float = 0

    num_vehicles: int = 10  # 10 para boa performance, max 22 para não fechar o cruzamento.

    def __init__(self, level):
        self.bg = pygame.image.load(level.image_path)
        self.paths = level.paths
        self.intersections = level.intersections
        self.lights = level.lights

    def get_lights(self):
        lights = []
        for intersection in self.intersections:
            lights.append(intersection.main_light)
            lights.append(intersection.secondary_light)
        return lights

    def calculate_start_point(self, point, path: List[Tuple[int, int]]):
        start_x, start_y = path[0]
        target_x, target_y = path[1]

        x_diff = target_x - start_x
        y_diff = target_y - start_y

        if y_diff == 0:
            y_diff = -0.01
        
        desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > start_y:
            desired_radian_angle += math.pi

        angle = math.degrees(desired_radian_angle+math.pi)
        start_point = (start_x - math.sin(math.radians(angle)) *
                       point, start_y - math.cos(math.radians(angle)) * point)
        return start_point

    def reset(self, level):
        for key, value in self.paths.items():
            path_code = key
            path = value

            points = [i*33 for i in range(1, (self.num_vehicles+1)*5)]
            points = random.sample(points, self.num_vehicles)

            for i in range(self.num_vehicles):

                start_point = [self.calculate_start_point(points[i], path)]
                vehicle_path = start_point + path

                vehicle = Vehicle(path_code=path_code, path=vehicle_path, MAX_SPEED=level.MAX_SPEED)
                self.vehicles.append(vehicle)

        return self.vehicles, self.intersections

    def draw_window(self):
        self.win.blit(self.bg, (0, 0))
        for vehicle in self.vehicles:
            vehicle.draw(self.win, (0, 116, 204))
            vehicle.draw_path(self.win)

        for light in self.lights:
            light.draw(self.win)

        pygame.display.update()

    def step(self, actions: Dict[str, int]):
        done = False

        if not self.vehicles:
            done = True
        
        if not done:
            for vehicle in self.vehicles:
                if vehicle.complete_path:
                    self.timer += vehicle.total_time
                    self.vehicles.remove(vehicle)
                    continue
                other_vehicles = self.vehicles[:]
                other_vehicles.remove(vehicle)
                vehicle.move(other_vehicles, self.lights)
                if vehicle.current_point >= 1:
                    vehicle.timer += 1

            for intersection in self.intersections:
                intersection.step(actions[intersection.id])

        reward = self.get_reward()

        return self.vehicles, self.intersections, reward, done

    def get_reward(self):
        if self.num_vehicles*len(self.paths)*self.FPS == 0:
            return 0
        return self.timer/(self.num_vehicles*len(self.paths)*self.FPS)
