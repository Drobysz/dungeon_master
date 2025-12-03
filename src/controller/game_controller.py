from typing import Dict, List, Tuple, Literal
from pathlib import Path

from load_levels import load_levels
from model.dungeon import Dungeon
from model.entities import Hero, Dragon

from time import sleep

Position = Tuple[int, int]
Results = Literal["win", "lose", ""]


class GameController:
    def __init__(s, level_path: Path, options: Dict) -> None:
        s.level_path: Path = level_path
        s.options:    Dict = options

        s.dungeon: Dungeon | None = None
        s.hero:    Hero | None = None
        s.dragons: List[Dragon] = []

        s.game_over:       bool = False
        s.game_result:     Results = ""
        s.next_path:       List[Position] = []
        s.is_moving:       bool = False
        s.dragon_prev_mvs: List[Position | None] = []
        
        
        s.nb_steps:       int = 0
        s.killed_dragons: int = 0
        s.shields:        int = 0

        s._load_level()


    @property
    def nb_dragons(s): return len(s.dragons)


    def _load_level(s) -> None:
        dungeon, hero, dragons = load_levels(s.level_path)
        s.dungeon = dungeon
        s.hero = hero
        s.dragons = dragons
        s.game_over = False
        s.game_result = ""
        s.nb_steps = 0
        s.killed_dragons = 0
        s.shields = 2
        s.dragon_prev_mvs = [ None for _ in range(len(s.dragons))]

    def reset(s) -> None:
        s._load_level()


    def rotate_cell(s, row: int, col: int) -> None:
        if s.dungeon is None:
            return

        s.dungeon.rotate_cell(row, col)


    def rotate_cell_from_pixel(s, x: int, y: int, cell_size: int) -> None:
        row = y // cell_size
        col = x // cell_size
        s.rotate_cell(row, col)


    def _next_step(s, r: int, c: int, pr: Position | None = None) -> Position | None:
        for (nbr_r, nbr_c), _ in s.dungeon.neighbors(r, c):
            if pr is not None and (nbr_r, nbr_c) == pr:
                continue

            if s.dungeon.are_connected(r, c, nbr_r, nbr_c):
                return(nbr_r, nbr_c)

        return None


    def compute_intention_path(s, max_steps: int = 1000) -> List[Position]:
        if s.dungeon is None or s.hero is None:
            return []

        row, col = s.hero["position"]
        path: List[Position] = []
        previous: Position | None = None
        steps = 0

        while steps < max_steps:
            next_pos: Position | None = s._next_step(row, col, previous)

            if next_pos is None:
                break

            path.append(next_pos)
            previous = (row, col)
            row, col = next_pos
            steps += 1

        return path


    def dragon_move(s) -> None:
        h_r, h_c = s.hero['position']
        h_lvl = s.hero['level']
        
        for idx, dragon in enumerate(s.dragons):
            r, c = dragon['position']
            d_lvl = dragon['level']
            prev = s.dragon_prev_mvs[idx]
            next_pos = s._next_step(r, c, prev) if s.options['dragons_move'] else (r, c)
            
            if next_pos is None:
                next_pos = (r, c)

            s.dragons[idx]['position'] = next_pos

            if s.options['dragons_move']:
                s.dragon_prev_mvs[idx] = (r, c)
            
            if next_pos is not None and (next_pos[0] == h_r and next_pos[1] == h_c):
                if h_lvl >= d_lvl:
                    s.hero['level'] = h_lvl + d_lvl
                    s.dragons.pop(idx)
                    s.killed_dragons += 1
                
                elif s.shields > 0:
                    s.shields -= 1
                    
                else:
                    s.game_over = True
                    s.game_result = "lose"
                    break
        
        if not s.game_over and not s.dragons:
            s.game_over = True
            s.game_result = "win"

    def end_turn(s, render) -> None:
        if s.game_over or s.dungeon is None or s.hero is None:
            return

        path = s.compute_intention_path()
        s.nb_steps += 1
        s.is_moving = True

        for step_row, step_col in path:
            s.hero["position"] = [step_row, step_col]

            sleep(0.3)
            render()

        s.is_moving = False

