from typing import Dict, List, Tuple


class Level:
    paths: Dict[str, List[Tuple[int, int]]]
    MAX_SPEED: int

class Level1(Level): 
    MAX_SPEED = 2
    paths = {
        "a": [(100, 100), (0, 250), (900, 250)],
        "b": [(0, 250), (450, 250), (450, 0)]
    }