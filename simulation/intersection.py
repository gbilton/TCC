import random
from typing import List
from uuid import uuid1

import torch

from simulation.ai.dqn import DQN
from simulation.ai.greedy import EpsilonGreedyStrategy
from simulation.light import TrafficLight
from simulation.ai.replaybuffer import ReplayBuffer
from helper.utils import TrafficLightState
from simulation.vehicle import Vehicle


class Intersection:
    yellow_time: float = 3.0 * 60
    yellow_timer: int = 0
    green_timer: int = 0
    num_actions = 2

    def __init__(self, main_light: TrafficLight, secondary_light: TrafficLight):
        self.id = uuid1()
        self.main_light = main_light
        self.secondary_light = secondary_light
        self.lights = [main_light, secondary_light]
        self.change_state: bool = False
        self.green_time_fps: float = self.calculate_green_time()
        self.policy_net = DQN()
        self.target_net = DQN()
        self.memory = ReplayBuffer(100000)
        self.strategy = EpsilonGreedyStrategy(start=1, end=0.01, decay=0.0001)
        self.optimizer = torch.optim.Adam(params=self.policy_net.parameters(), lr=0.001)
        self.current_step = 0
        self.timer = 0
        self.min_time = 60

    def step(self, action: int):
        self.timer += 1

        for light in self.lights:
            light.timer += 1

        if action == 1 or self.change_state:
            self.change_state = True
            self.sync_lights()

    def method(self, method_name: str, *args):
        foo = getattr(self, method_name)
        return foo(*args)

    def random_action(self, *args) -> int:
        action = 0
        a = random.normalvariate(50, 10)
        if a > 75:
            action = 1
        return action

    def select_action(self, vehicles: List[Vehicle]) -> int:
        if self.timer < self.min_time:
            return 0
        rate = self.strategy.get_exploration_rate(self.current_step)
        self.current_step += 1
        if rate > random.random():
            # explore
            return random.randrange(self.num_actions)
        else:
            observation = self.get_observation(vehicles)
            # exploit
            with torch.no_grad():
                return self.policy_net.act(observation)

    def calculate_green_time(self):
        qi: float = 600  # fluxo na aproximação (veículo/h)
        L: int = 10  # largura da intersecção em metros
        total_red_time: float = 60
        perception_time: int = 2  # tempo de percepção: 2 segundos

        green_time = (
            qi
            / (525 * L)
            * (
                (1.5 * (total_red_time + perception_time) + 5 - total_red_time + perception_time)
                / (1 - (qi / (525 * L)))
            )
            + perception_time
            + (self.yellow_time / 60)
        )

        green_time_fps = green_time * 60
        return green_time_fps

    def formal_action(self, *args):
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
                self.timer = 0
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
                self.timer = 0
            else:
                self.yellow_timer += 1

    def get_observation(self, vehicles: List[Vehicle]):

        total_num_vehicles = 0
        total_speed = 0
        total_num_red_light_vehicles = 0
        for light in self.lights:
            (
                num_vehicles,
                speed,
                num_red_light_vehicles,
                state_timer,
            ) = light.get_sensor_info(vehicles)

            total_num_vehicles += num_vehicles
            total_speed += speed
            total_num_red_light_vehicles += num_red_light_vehicles

        if total_num_vehicles != 0:
            total_avg_speed = total_speed / total_num_vehicles
        else:
            total_avg_speed = 0

        observation = [
            total_num_vehicles,
            total_avg_speed,
            num_red_light_vehicles,
            state_timer,
        ]

        return [i / 10 for i in observation]

    def get_current(self, states, actions):
        return self.policy_net(states).gather(dim=1, index=actions)

    def get_next(self, next_states):
        return self.target_net(next_states).max(dim=1, keepdim=True).values

    def update_target_net(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def load_model(self, model_path):
        checkpoint = torch.load(model_path)
        self.policy_net.load_state_dict(checkpoint["policy_net"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
