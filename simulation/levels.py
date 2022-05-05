from typing import Dict, List, Tuple
from simulation.intersection import Intersection

from simulation.light import TrafficLight
from helper.utils import IncomingTraffic, TrafficLightState


class Level:
    paths: Dict[str, List[Tuple[int, int]]]
    MAX_SPEED: int


class Level1(Level):
    MAX_SPEED = 1
    image_path = "images/level 1.png"
    paths = {
        "a": [(1, 303), (444, 316), (898, 331)],
        "b": [(475, 4), (464, 297), (468, 497)],
    }
    lights: List[TrafficLight] = [
        TrafficLight((444, 316), TrafficLightState.green, IncomingTraffic.west),
        TrafficLight((464, 297), TrafficLightState.red, IncomingTraffic.north),
    ]
    intersections: List[Intersection] = [
        Intersection(main_light=lights[0], secondary_light=lights[1])
    ]


class Level2(Level):
    MAX_SPEED = 1
    image_path = "images/level 2.png"
    paths = {
        "a": [(193, 4), (183, 286), (182, 496)],
        "b": [(0, 298), (165, 305), (765, 322), (899, 330)],
        "c": [(780, 498), (783, 343), (796, 2)],
    }
    lights: List[TrafficLight] = [
        TrafficLight((165, 305), TrafficLightState.green, IncomingTraffic.west),
        TrafficLight((183, 286), TrafficLightState.red, IncomingTraffic.north),
        TrafficLight((765, 322), TrafficLightState.green, IncomingTraffic.west),
        TrafficLight((783, 343), TrafficLightState.red, IncomingTraffic.south),
    ]
    intersections: List[Intersection] = [
        Intersection(main_light=lights[0], secondary_light=lights[1]),
        Intersection(main_light=lights[2], secondary_light=lights[3]),
    ]
