from typing import Dict, List, Tuple, Literal
from pathlib import Path

from load_levels import load_levels
from model.dungeon import Dungeon
from model.entities import Hero, Dragon

Position = Tuple[int, int]
Results = Literal["win", "lose", ""]


class GameController:
    def __init__(s, level_path: Path, options: Dict) -> None:
        s.level_path: Path = level_path
        s.options: Dict = options

        s.dungeon: Dungeon | None = None
        s.hero: Hero | None = None
        s.dragons: List[Dragon] = []

        s.game_over: bool = False
        s.game_result: Results = ""
        s.last_path: List[Position] = []

        s._load_level()


    def _load_level(s) -> None:
        dungeon, hero, dragons = load_levels(s.level_path)
        s.dungeon = dungeon
        s.hero = hero
        s.dragons = dragons
        s.game_over = False
        s.game_result = ""


    def reset(s) -> None:
        s._load_level()


    def rotate_cell(s, row: int, col: int) -> None:
        if s.dungeon is None:
            return

        if not s.dungeon.in_bound(row, col):
            return

        s.dungeon.rotate_cell(row, col)


    def rotate_cell_from_pixel(s, x: int, y: int, cell_size: int) -> None:
        row = y // cell_size
        col = x // cell_size
        s.rotate_cell(row, col)


    def _compute_intention_path(s, max_steps: int = 1000) -> List[Position]:
        if s.dungeon is None or s.hero is None:
            return []

        row, col = s.hero["position"]
        path: List[Position] = []
        previous: Position | None = None
        steps = 0

        while steps < max_steps:
            next_pos: Position | None = None

            for (nbr_row, nbr_col), _ in s.dungeon.neighbors(row, col):
                if previous is not None and (nbr_row, nbr_col) == previous:
                    continue
                if s.dungeon.are_connected(row, col, nbr_row, nbr_col):
                    next_pos = (nbr_row, nbr_col)
                    break

            if next_pos is None:
                break

            path.append(next_pos)
            previous = (row, col)
            row, col = next_pos
            steps += 1

        return path


    def end_turn(s) -> None:
        if s.game_over or s.dungeon is None or s.hero is None:
            return

        path = s._compute_intention_path()
        s.last_path = path

        hero_lvl = s.hero["level"]

        for step_row, step_col in path:
            s.hero["position"] = [step_row, step_col]

            dragon_idx = None
            dragon_lvl = 0
            for idx, dragon in enumerate(s.dragons):
                d_row, d_col = dragon["position"]
                if d_row == step_row and d_col == step_col:
                    dragon_idx = idx
                    dragon_lvl = int(dragon["level"])
                    break

            if dragon_idx is not None:
                if hero_lvl >= dragon_lvl:
                    s.hero["level"] = hero_lvl + dragon_lvl
                    s.dragons.pop(dragon_idx)

                else:
                    s.game_over = True
                    s.game_result = "lose"
                    break

        if not s.game_over and not s.dragons:
            s.game_over = True
            s.game_result = "win"

    def is_over(s) -> bool:
        return s.game_over