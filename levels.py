from typing import Dict, List, Tuple

from light import TrafficLight
from utils import TrafficLightState


class Level:
    paths: Dict[str, List[Tuple[int, int]]]
    MAX_SPEED: int

class Level1(Level): 
    MAX_SPEED = 1
    paths = {
        "a": [(1, 303), (444, 316), (898, 331)],
        "b": [(475, 4), (464, 297), (468, 497)] 
    }
    image_path = "images/level 1.png"

    lights: List[TrafficLight] = [
        TrafficLight((444, 316), TrafficLightState.green),
        TrafficLight((464, 297), TrafficLightState.red)
    ]

class Level2(Level):
    MAX_SPEED = 1
    paths = {
        "a": [(193, 4), (183, 286), (182, 496)],
        "b": [(0, 298), (165, 305), (765, 322), (899, 330)],
        "c": [(780, 498), (783, 343), (796, 2)] 
    }
    image_path = "images/level 2.png"

    lights: List[TrafficLight] = [
        TrafficLight((165, 305), TrafficLightState.green),
        TrafficLight((183, 286), TrafficLightState.red),
        TrafficLight((765, 322), TrafficLightState.green),
        TrafficLight((783, 343), TrafficLightState.red)
    ]