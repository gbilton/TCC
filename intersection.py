import random
from typing import List, Optional

from dqn import DQN
from light import TrafficLight
from utils import TrafficLightState
from vehicle import Vehicle


class Intersection:
    yellow_time: float = 3.0 * 60
    yellow_timer: int = 0
    green_timer: int = 0

    def __init__(self, main_light: TrafficLight, secondary_light: TrafficLight):
        self.main_light = main_light
        self.secondary_light = secondary_light
        self.lights = [main_light, secondary_light]
        self.change_state: bool = False
        self.green_time_fps: float = self.calculate_green_time()
        self.policy_net = DQN()

    def step(self, vehicles: Optional[List[Vehicle]] = None):
        for light in self.lights:
            light.timer += 1

        if not self.change_state:
            # self.random_change()
            # self.formal_change()
            self.ai_change(vehicles)
        self.sync_lights()

    def random_change(self):
        a = random.normalvariate(50, 10)
        if a > 75:
            self.change_state = True

    def ai_change(self, vehicles: List[Vehicle]):
        observation = self.get_observation(vehicles)
        normalized_observation = [i/10 for i in observation]
        action = self.policy_net.act(normalized_observation)
        if action == 1:
            self.change_state = True

    def calculate_green_time(self):
        qi: float = 600  # fluxo na aproximação (veículo/h)
        L: int = 10  # largura da intersecção em metros
        total_red_time: float = 60
        perception_time: int = 2  # tempo de percepção: 2 segundos

        green_time = qi/(525*L)*((1.5*(total_red_time + perception_time)+5-total_red_time +
                                  perception_time)/(1-(qi/(525*L))))+perception_time+(self.yellow_time/60)

        green_time_fps = green_time * 60
        return green_time_fps
    
    def formal_change(self):
        if self.green_timer >= self.green_time_fps:
            self.change_state = True
            self.green_timer = 0
        else:
            self.green_timer += 1

    def sync_lights(self):
        if not self.change_state:
            return
        
        if self.main_light.state == TrafficLightState.green:
            self.main_light.change_color()
            self.yellow_timer = 0
            
        elif self.main_light.state == TrafficLightState.yellow:
            if self.yellow_timer >= self.yellow_time:
                self.main_light.change_color()
                self.secondary_light.change_color()
                self.change_state = False
            else:
                self.yellow_timer += 1

        elif self.secondary_light.state == TrafficLightState.green:
            self.secondary_light.change_color()
            self.yellow_timer = 0
        
        elif self.secondary_light.state == TrafficLightState.yellow:
            if self.yellow_timer >= self.yellow_time:
                self.secondary_light.change_color()
                self.main_light.change_color()
                self.change_state = False
            else:
                self.yellow_timer += 1

    def get_observation(self, vehicles: List[Vehicle]):
        total_num_vehicles = 0
        total_speed = 0
        total_num_red_light_vehicles = 0
        for light in self.lights:
            num_vehicles, speed, num_red_light_vehicles, state_timer = light.get_sensor_info(
            vehicles)
            
            total_num_vehicles += num_vehicles
            total_speed += speed
            total_num_red_light_vehicles += num_red_light_vehicles

        if total_num_vehicles != 0:
            total_avg_speed = total_speed / total_num_vehicles
        else: 
            total_avg_speed = 0
            
        observation = [total_num_vehicles, total_avg_speed, num_red_light_vehicles, state_timer]

        return observation