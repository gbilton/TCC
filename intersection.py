import random
from light import TrafficLight
from utils import TrafficLightState


class Intersection:
    yellow_time: int = 5 * 60
    yellow_timer: int = 0

    def __init__(self, main_light: TrafficLight, secondary_light: TrafficLight):
        self.main_light = main_light
        self.secondary_light = secondary_light
        self.change_state: bool = False

    def random_change(self):
        if not self.change_state:
            a = random.normalvariate(50, 10)
            if a > 80:
                self.change_state = True
        # self.change_state = True
        self.sync_lights()

    def sync_lights(self):
        if not self.change_state:
            return
        
        if self.main_light.state == TrafficLightState.green:
            self.main_light.state = TrafficLightState.yellow
            self.yellow_timer = 0
            
        elif self.main_light.state == TrafficLightState.yellow:
            if self.yellow_timer >= self.yellow_time:
                self.main_light.state = TrafficLightState.red
                self.secondary_light.state = TrafficLightState.green
                self.change_state = False
            else:
                self.yellow_timer += 1
                print(self.yellow_timer)

        elif self.secondary_light.state == TrafficLightState.green:
            self.secondary_light.state = TrafficLightState.yellow
            self.yellow_timer = 0
        
        elif self.secondary_light.state == TrafficLightState.yellow:
            if self.yellow_timer >= self.yellow_time:
                self.secondary_light.state = TrafficLightState.red
                self.main_light.state = TrafficLightState.green
                self.change_state = False
            else:
                self.yellow_timer += 1