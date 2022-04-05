from typing import Dict, List, Tuple


class Level:
    paths: Dict[str, List[Tuple[int, int]]]
    MAX_SPEED: int

class Level1(Level): 
    MAX_SPEED = 2
    paths = {
        "a": [(0, 250), (450, 250), (450, 20)],
        # "b": [(0, 250), (450, 250), (450, 0)]
    }