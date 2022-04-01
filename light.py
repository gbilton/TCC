from typing import Tuple

import pygame
from pygame.draw import circle

from utils import TrafficLightState


class TrafficLight:
    radius: int = 10
    def __init__(self, position: Tuple[int, int], state: TrafficLightState):
        self.x = position[0]
        self.y = position[1]
        self.state = state
    

    def draw(self, surface):
        position = (self.x, self.y)
        circle(surface, self.state, position, self.radius)
    

    def change_state(self):
        if self.state == TrafficLightState.green:
            self.state = TrafficLightState.yellow
        elif self.state == TrafficLightState.yellow:
            self.state = TrafficLightState.red
        elif self.state == TrafficLightState.red:
            self.state = TrafficLightState.green

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y-self.radius, self.radius*2, self.radius*2)
