from typing import Tuple, List, Dict
from pathlib import Path

from model.dungeon import Dungeon
from model.cell import Cell

import json
from helpers import get_filename, get_complete_path, convert_map

GridSrc = List[List[dict]]
Grid = List[List[Cell]]

def load_levels(path: str | Path) -> Tuple[Dungeon, Dict, List]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    lvl_name = get_filename(path)
    map_path = get_complete_path(f"levels/{lvl_name}.txt")
    grid_src: GridSrc = convert_map(map_path)

    grid: Grid = [
        [
            Cell(
                n = el["top"],
                e = el["right"],
                s = el["bottom"],
                w = el["left"]
            ) for el in row
        ] for row in grid_src
    ]
        
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
    