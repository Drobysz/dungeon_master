from dataclasses import dataclass
from typing import Tuple, List
from pathlib import Path

Pos = Tuple[int, int]

@dataclass
class Hero:
    positon: Pos
    level: int = 1
    
@dataclass
class Dragon:
    positon: Pos
    level: int
    
@dataclass
class Diamonds:
    positions: List[Pos]
    nb: int
    isActivated: bool
    img: Path