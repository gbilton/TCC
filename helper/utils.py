from collections import namedtuple
from enum import Enum
from typing import Tuple

import torch


class TrafficLightState(Tuple, Enum):
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    red = (255, 0, 0)


class IncomingTraffic(str, Enum):
    north = "north"
    south = "south"
    east = "east"
    west = "west"


Experience = namedtuple(
    "Experience", ("state", "action", "next_state", "reward", "done")
)


def extract_tensors(experiences):

    batch = Experience(*zip(*experiences))

    t1 = torch.cat(batch.state)
    t2 = torch.cat(batch.action)
    t3 = torch.cat(batch.reward)
    t4 = torch.cat(batch.next_state)
    t5 = batch.done
    return (t1, t2, t3, t4, t5)


def np_to_torch(state, device):
    state = torch.tensor(state, dtype=torch.float32)
    # state = torch.reshape(state, (1, len(state)))
    state = state.to(device)
    return state
