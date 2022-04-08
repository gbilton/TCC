from typing import Tuple

import pygame
from pygame.draw import circle

from utils import TrafficLightState


class TrafficLight:
    radius: int = 3
    timer: int = 0
    green_time: int = 300
    yellow_time: int = 100

    def __init__(self, position: Tuple[int, int], state: TrafficLightState):
        self.x = position[0]
        self.y = position[1]
        self.state = state

    def draw(self, surface):
        position = (self.x, self.y)
        circle(surface, self.state, position, self.radius)
    
    # def change_state(self):
    #     self.random_state_change()

    def change_color(self):
        if self.state == TrafficLightState.green:
            self.state = TrafficLightState.yellow
        elif self.state == TrafficLightState.yellow:
            self.state = TrafficLightState.red
        elif self.state == TrafficLightState.red:
            self.state = TrafficLightState.green

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y-self.radius, self.radius*2, self.radius*2)


    def law_state_change(self):
        pass

    def ai_state_change(self):
        pass