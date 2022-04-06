from typing import Dict, List, Tuple

from light import TrafficLight
from utils import TrafficLightState


class Level:
    paths: Dict[str, List[Tuple[int, int]]]
    MAX_SPEED: int

class Level1(Level): 
    MAX_SPEED = 0.5
    paths = {
        "a": [(1, 303), (444, 316), (898, 331)],
        "b": [(475, 4), (464, 297), (468, 497)] 
    }
    image_path = "images/level 1.png"

    lights: List[TrafficLight] = [
        TrafficLight((444, 316), TrafficLightState.green),
        TrafficLight((464, 297), TrafficLightState.red)
    ]