from typing import Tuple, List, Dict
from pathlib import Path
from .dungeon import Dungeon
from .cell import Cell
import json

GridSrc = List[List[dict]]
Grid = List[List[Cell]]

def load_levels(path: Path) -> Tuple[Dungeon, Dict, List]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    grid_src: GridSrc = data
    grid: Grid = []
    
    for row in grid_src:
        grid.append([
            Cell(
                north = el["top"],
                east = el["right"],
                south = el["bottom"],
                west = el["left"]
            ) for el in row
        ])
        
    dungeon = Dungeon(grid)
    
    return dungeon, {"level": 1, "position": [0, 0]}, []
    