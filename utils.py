from enum import Enum
from typing import Tuple


class TrafficLightState(Tuple, Enum):
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    red = (255, 0, 0)
