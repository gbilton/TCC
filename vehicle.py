import math
from typing import List, Tuple
from pygame.draw import circle
import pygame


class Vehicle:
    def __init__(self, start_position, end_position, max_speed, acceleration):
        self.speed: float = 0
        self.start_position: Tuple[int, int] = start_position
        self.end_position: Tuple[int, int] = end_position
        self.max_speed: int = max_speed
        self.acceleration: float = acceleration
        self.x: float = start_position[0]
        self.y: float = start_position[1]
        self.path: List[Tuple[int, int]] = self.generate_path()
        self.angle = 0
        self.rotation_vel = 4
        self.current_point = 0
        self.radius = 10
        self.timer = 0
        self.complete_path = False


    def draw(self, surface, color):
        position = (self.x, self.y)
        circle(surface, color, position, self.radius)


    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel


    def calculate_angle(self):
        try:
            target_x, target_y = self.path[self.current_point]
        except IndexError:
            self.complete_path = True
            exit()

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
        target = self.path[self.current_point]
        rect = pygame.Rect(
            self.x, self.y, self.radius*2, self.radius*2)
        if rect.collidepoint(*target):
            self.current_point += 1


    def move(self):
        self.speed = min(self.speed + self.acceleration, self.max_speed)

        self.calculate_angle()
        self.update_path_point()
        
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.speed
        horizontal = math.sin(radians) * self.speed

        self.y -= vertical
        self.x -= horizontal


    def generate_path(self):
        path = [self.start_position, self.end_position]
        return path


    def add_point(self, point):
        self.path.append(point)


    def draw_path(self, surface):
        for point in self.path[self.current_point:]:
            circle(surface, (0,0,0), point, 4)
