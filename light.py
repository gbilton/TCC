from typing import List, Tuple

import pygame
from pygame.draw import circle

from utils import IncomingTraffic, TrafficLightState
from vehicle import Vehicle


class TrafficLight:
    radius: int = 3
    timer: int = 0
    green_time: int = 300
    yellow_time: int = 100
    radar_distance: int = 200

    def __init__(self, position: Tuple[int, int], state: TrafficLightState, incoming_traffic_direction: IncomingTraffic):
        self.x = position[0]
        self.y = position[1]
        self.state = state
        self.incoming_traffic_direction = incoming_traffic_direction
        self.traffic_rect = self.get_traffic_rect()

    def draw(self, surface):
        position = (self.x, self.y)
        circle(surface, self.state, position, self.radius)
        pygame.draw.rect(surface, (255, 255, 0), self.get_traffic_rect())
    
    def change_color(self):
        if self.state == TrafficLightState.green:
            self.state = TrafficLightState.yellow
        elif self.state == TrafficLightState.yellow:
            self.state = TrafficLightState.red
            self.timer = 0
        elif self.state == TrafficLightState.red:
            self.state = TrafficLightState.green
            self.timer = 0

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y-self.radius, self.radius*2, self.radius*2)

    def get_traffic_rect(self):
        if self.incoming_traffic_direction == IncomingTraffic.north:
            return pygame.Rect(self.x - self.radius, self.y-self.radius - self.radar_distance, self.radius*2, self.radar_distance)
        elif self.incoming_traffic_direction == IncomingTraffic.south:
            return pygame.Rect(self.x - self.radius, self.y-self.radius, self.radius*2, self.radar_distance)
        elif self.incoming_traffic_direction == IncomingTraffic.east:
            return pygame.Rect(self.x - self.radius, self.y-self.radius, self.radar_distance, self.radius*2)
        elif self.incoming_traffic_direction == IncomingTraffic.west:
            return pygame.Rect(self.x - self.radius - self.radar_distance, self.y-self.radius, self.radar_distance, self.radius*2)

    def get_sensor_info(self, vehicles: List[Vehicle]):
        num_vehicles = 0 
        speed = 0
        num_red_light_vehicles = 0
        for vehicle in vehicles:
            if self.traffic_rect.colliderect(vehicle.get_rect()):
                num_vehicles += 1
                speed += abs(vehicle.speed)
                if self.state == TrafficLightState.red:
                    num_red_light_vehicles += 1
        state_time = self.timer/60
        return num_vehicles, speed, num_red_light_vehicles, state_time