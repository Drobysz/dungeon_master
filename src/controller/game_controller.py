from typing import Dict, List, Tuple, Literal
from pathlib import Path

from load_levels import load_levels
from model.dungeon import Dungeon
from model.entities import Hero, Dragon

from helpers import \
    list_files, \
    get_complete_path

Position = Tuple[int, int]
Animations = Literal["attack", "shield", "walk", "none"]
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
        s.dragon_prev_mvs: List[Position | None] = []
        
        s.nb_steps:       int = 0
        s.killed_dragons: int = 0
        s.shields:        int = 0
        
        s.tick:         int = 0
        s.dragon_tick:  int = 0
        s.walking_tick: int = 0
        s.clash_tick:   int = 0
        
        s.dragon_frames:      Dict[List[Path]] = []
        s.dragron_frame_nb:   int = 0
        s.encountered_dragon: int = None
        
        s.hero_anims:      Dict[Animations, List[Path]] = []
        s._hero_curr_anim: Animations = "none"
        s.hero_frame_nb:   int = 0
        
        s._in_clash:  bool = False
        s._is_moving: bool = False

        s._load_level()


    def _load_level(s) -> None:
        dungeon, hero, dragons = load_levels(s.level_path)
        s.dungeon = dungeon
        s.hero    = hero
        s.dragons = dragons

        s.game_over = False
        s.game_result = ""
        s.nb_steps = 0
        s.killed_dragons = 0
        s.shields = 2
        s.is_moving = False
        s.dragon_prev_mvs = [None for _ in range(len(s.dragons))]
        
        s.tick = 0
        s.dragon_tick = 0 
        s.walking_tick = 0
        s.clash_tick = 0

        s.dragon_frames = [
            list_files(
                path=f"assets/dragon_frames/{str(idx + 1)}",
                ext="png"
            )
            for idx in range(8)
        ]
        s.dragron_frame_nb = 0
        s.encountered_dragon = None
        
        s.hero_anims = {
            a: list_files(
                path=f"assets/knight/frames/{a}",
                ext="png",
            )
            for a in ["attack", "shield", "walk"]
        }
        s.hero_anims["none"] = get_complete_path("assets/knight/hero.png")
        s.hero_frame_nb = "none"
        
        s.in_clash = False
        
        
    def reset(s) -> None:
        s._load_level()
        

    @property
    def nb_dragons(s) -> int:
        return len(s.dragons)
    
    @property
    def hero_frame_qntty(s) -> int:
        if s.hero_curr_anim != "none":
            return len(s.hero_anims[s.hero_curr_anim])
        else:
            return 1
    
    @property
    def hero_curr_anim(s) -> Animations:
        return s._hero_curr_anim

    @hero_curr_anim.setter
    def hero_curr_anim(s, anim: Animations) -> None:
        if s._hero_curr_anim != anim:
            s._hero_curr_anim = anim
            s.hero_frame_nb = 0
    
    @property
    def in_clash(s):
        return s._in_clash
    
    @in_clash.setter
    def in_clash(s, state: bool) -> None:
        s._in_clash = state
        
        if not state:
            s.hero_curr_anim = "walk" if s.is_moving else "none"
            s.clash_tick = 0
            
            if not s.game_over and not s.dragons:
                s.game_over = True
                s.game_result = "win"
    
    @property
    def is_moving(s):
        return s._is_moving
    
    @is_moving.setter
    def is_moving(s, state):
        s.walking_tick = 0
        s._is_moving = state
        

    def get_hero_frame(s) -> Path | str:
        animation = s.hero_curr_anim
        if animation == "none":
            return s.hero_anims[animation]

        frames = s.hero_anims[animation]
        s.hero_frame_nb = (s.hero_frame_nb + 1) % s.hero_frame_qntty

        return frames[s.hero_frame_nb]
    
    def get_dragon_frame(s) -> int:
        if s.dragon_tick % 10 == 0:
            s.dragron_frame_nb = (s.dragron_frame_nb + 1) % 4
        
        return s.dragron_frame_nb


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


    def detect_clash_and_winner(s, render):
        h_r, h_c = s.hero['position']
        h_lvl = s.hero['level']
    
        for idx, dragon in enumerate(s.dragons):
            d_r, d_c = dragon['position']
            d_lvl = dragon['level']
            equal_coord = d_r == h_r and d_c == h_c
            
            if not equal_coord and idx == s.encountered_dragon:
                s.encountered_dragon = None
            
            if dragon['position'] is not None\
                and equal_coord\
                and s.encountered_dragon != idx:
                s.encountered_dragon = idx
                
                if h_lvl >= d_lvl:
                    s.hero_curr_anim = "attack"
                    s.hero['level'] = h_lvl + d_lvl
                    s.encountered_dragon = None
                    s.dragons.pop(idx)
                    s.killed_dragons += 1
                
                elif s.shields > 0:
                    s.hero_curr_anim = "shield"
                    s.shields -= 1
                    
                else:
                    s.game_over = True
                    s.game_result = "lose"
                
                duration = 10 if s.hero_curr_anim == "attack" else 5
                s.in_clash = True
                
                
                while s.clash_tick != duration:
                    render()
                    
                s.in_clash = False
                    
                if s.game_over:
                    break
                

    def dragon_move(s) -> None:
        for idx, dragon in enumerate(s.dragons):
            if s.encountered_dragon is not None\
                and s.encountered_dragon == idx:
                    continue
            
            r, c = dragon['position']
            prev = s.dragon_prev_mvs[idx]

            dragon['position'] = s._next_step(r, c, prev)
            if dragon['position'] is not None:
                s.dragon_prev_mvs[idx] = (r, c)
            else:
                dragon['position'] = (r, c)
                s.dragon_prev_mvs[idx] = None


    def anim_exec(func):
        def wrapper(s: "GameController", *args, **kwargs):
            s.nb_steps += 1
            s.is_moving = True
            s.hero_curr_anim = "walk"

            func(s, *args, **kwargs)

            s.is_moving = False
            s.hero_curr_anim = "none"
        
        return wrapper

    @anim_exec
    def end_turn(s, render) -> None:
        if s.game_over or s.dungeon is None or s.hero is None:
            return

        path = s.compute_intention_path()

        for step_row, step_col in path:
            s.hero["position"] = [step_row, step_col]
            s.walking_tick = 0

            while s.walking_tick <= 30:
                render()


    def ticking(s, render):
        s.tick = (s.tick + 1) % 30
        s.dragon_tick = (s.dragon_tick + 1) % 30
        
        if not s.in_clash and not s.game_over:
            s.detect_clash_and_winner(render)
    
        if s.tick % 30 == 0 and s.options['dragons_move']:
            s.dragon_move()
        
        if s.is_moving:
            s.walking_tick += 1
        
        if s.in_clash:
            s.clash_tick += 1
