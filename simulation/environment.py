import math
from typing import Dict, List, Tuple
import random
from uuid import UUID

import pygame

from simulation.vehicle import Vehicle


class Environment:
    pygame.display.set_caption("Semáforo Autônomo")
    WIDTH, HEIGHT = 900, 500
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    render: bool = True
    FPS: int = 60
    timer: float = 0
    num_vehicles: int = 5  # 10 para boa performance, max 22 para não fechar o cruzamento.
    vehicles: List[Vehicle] = []
    paths: Dict[str, List[Tuple[int, int]]]

    def __init__(self, level):
        self.bg = pygame.image.load(level.image_path)
        self.paths = level.paths
        self.intersections = level.intersections
        self.lights = level.lights

    def reset(self, level):
        self.timer = 0
        for key, value in self.paths.items():
            path_code = key
            path = value

            # points = [i * 33 for i in range(1, (self.num_vehicles + 1) * 5)]
            # points = random.sample(points, self.num_vehicles)
            points = [330, 627, 792, 165, 660]
            for i in range(self.num_vehicles):
                start_point = [self._calculate_start_point(points[i], path)]
                vehicle_path = start_point + path  # type: ignore

                vehicle = Vehicle(path_code=path_code, path=vehicle_path, MAX_SPEED=level.MAX_SPEED)
                self.vehicles.append(vehicle)

        return self.vehicles, self.intersections

    def step(self, actions: Dict[UUID, int]):
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

        reward = self.get_reward(done)

        return self.vehicles, reward, done

    def get_lights(self):
        lights = []
        for intersection in self.intersections:
            lights.append(intersection.main_light)
            lights.append(intersection.secondary_light)
        return lights

    def _calculate_start_point(self, point, path: List[Tuple[int, int]]):
        start_x, start_y = path[0]
        target_x, target_y = path[1]

        x_diff = target_x - start_x
        y_diff: float = target_y - start_y

        if y_diff == 0:
            y_diff = -0.01

        desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > start_y:
            desired_radian_angle += math.pi

        angle = math.degrees(desired_radian_angle + math.pi)
        start_point = (
            start_x - math.sin(math.radians(angle)) * point,
            start_y - math.cos(math.radians(angle)) * point,
        )
        return start_point

    def draw_window(self):
        self.win.blit(self.bg, (0, 0))
        for vehicle in self.vehicles:
            vehicle.draw(self.win, (0, 116, 204))
            vehicle.draw_path(self.win)

        for light in self.lights:
            light.draw(self.win)

        pygame.display.update()

    def get_reward(self, done) -> float:
        if done:
            return -1 * self.timer / (self.num_vehicles * len(self.paths) * self.FPS)
        else:
            speeds = [vehicle.speed for vehicle in self.vehicles]
            avg_speed = sum(speeds) / len(speeds)
            return avg_speed
