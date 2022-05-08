import math
from typing import List, Tuple
from pygame.draw import circle
from pygame.surface import Surface
import pygame

from helper.utils import TrafficLightState


class Vehicle:
    acceleration: float = 0.01
    breaking: float = 0.1
    rotation_vel: int = 5
    radius: float = 10.78
    MIN_SPEED = 0
    SIGHT_COEF: float = radius * 5
    MIN_SIGHT: float = radius + 4.31

    def __init__(self, path_code: str, path: List[Tuple[int, int]], MAX_SPEED: int):
        self.path_code = path_code
        self.path = path
        self.MAX_SPEED = MAX_SPEED
        self.speed: float = 0
        self.x: float = path[0][0]
        self.y: float = path[0][1]
        self.current_point: int = 0
        self.angle: float = self.calculate_initial_angle()
        self.timer = 0
        self.complete_path = False

    def get_rect(self):
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )

    def calculate_initial_angle(self):
        target_x, target_y = self.path[1]

        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        return math.degrees(desired_radian_angle)

    def draw(self, surface: Surface, color: Tuple[int, int, int]):
        position = (self.x, self.y)
        circle(surface, color, position, self.radius)

        # Draw rect
        # pygame.draw.rect(surface, (255, 0, 0), self.get_rect())

        # Draw sight
        # points = self.sight()
        # for point in points:
        #     circle(surface, (0,255, 0), point, 2)

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def calculate_angle(self):
        if self.current_point > len(self.path) - 1:
            self.complete_path = True
            self.total_time = self.timer
            return
        target_x, target_y = self.path[self.current_point]
        # self.complete_path = True
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        if self.complete_path:
            return
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        if rect.collidepoint(*target):
            self.current_point += 1

    def accelerate(self):
        self.speed = min(self.speed + self.acceleration, self.MAX_SPEED)

    def detect_red_light(self, lights):
        if lights:
            for light in lights:
                points = self.sight()
                rect = light.get_rect()
                for point in points:
                    if rect.collidepoint(point):
                        if light.state == TrafficLightState.red:
                            return True
                        elif (
                            light.state == TrafficLightState.yellow
                            and points.index(point) > len(points) / 1.5
                        ):
                            return True
            return False

    def move(self, vehicles, lights):
        if self.detect_traffic(vehicles):
            self.brake()
        elif self.detect_red_light(lights):
            self.brake()
        else:
            self.accelerate()

        self.calculate_angle()
        self.update_path_point()

        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.speed
        horizontal = math.sin(radians) * self.speed

        self.y -= vertical
        self.x -= horizontal

    def add_point(self, point):
        self.path.append(point)

    def draw_path(self, surface):
        for point in self.path[self.current_point :]:
            circle(surface, (0, 0, 0), point, 4)

    def detect_traffic(self, vehicles):
        if vehicles:
            for vehicle in vehicles:
                if vehicle.path_code == self.path_code:
                    points = self.sight()
                    rect = vehicle.get_rect()
                    for point in points:
                        if rect.collidepoint(point):
                            if abs(vehicle.angle - self.angle) < 10:
                                return True

        return False

    def get_sight_distance(self):
        return int(self.SIGHT_COEF * self.speed + self.MIN_SIGHT)

    def sight(self):
        points = list(range(0, self.get_sight_distance()))
        return [
            (
                self.x - math.sin(math.radians(self.angle)) * point,
                self.y - math.cos(math.radians(self.angle)) * point,
            )
            for point in points
        ]

    def brake(self):
        self.speed = max(self.speed - self.breaking, self.MIN_SPEED)

    def detect_traffic_light(self):
        pass


class Car(Vehicle):
    pass


class Truck(Vehicle):
    pass


class Bike(Vehicle):
    pass
