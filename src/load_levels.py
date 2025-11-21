from typing import Tuple, List, Dict
from pathlib import Path
from model.dungeon import Dungeon
from model.cell import Cell
import json

GridSrc = List[List[dict]]
Grid = List[List[Cell]]

def load_levels(path: str | Path) -> Tuple[Dungeon, Dict, List]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    grid_src: GridSrc = data["grid"]
    grid: Grid = []
    
    for row in grid_src:
        grid.append([
            Cell(
                n = el["top"],
                e = el["right"],
                s = el["bottom"],
                w = el["left"]
            ) for el in row
        ])
        
    dungeon = Dungeon(grid)
    hero_data = data["hero"]
    hero = {
        "level": hero_data["level"],
        "position": [hero_data["row"], hero_data["col"]]
    }
    dragons = [
        {
            "level": el["level"],
            "position": [el["row"], el["col"]]
        }
        for el in data["dragons"]
    ]
    
    return dungeon, hero, dragons
    