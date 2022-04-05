from typing import Dict, List, Tuple


class Level:
    paths: Dict[str, List[Tuple[int, int]]]
    MAX_SPEED: int

class Level1(Level): 
    MAX_SPEED = 0.5
    paths = {
        "a": [(50, 250), (900, 250)],
        "b": [(450, 50), (450, 500)] 
    }