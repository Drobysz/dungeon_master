from dataclasses import dataclass
from typing import Tuple

Pos = Tuple[int, int]

@dataclass
class Hero:
    positon: Pos
    level: int = 1
    
@dataclass
class Dragon:
    positon: Pos
    level: int