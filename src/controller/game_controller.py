from typing import Dict, List
from pathlib import Path
from .classes import *

from model.dungeon import Dungeon
from model.entities import Hero, Dragon, Diamonds

from load_levels import load_levels
from helpers import \
    list_files, \
    get_complete_path



class GameController:
    def __init__(s, level_path: Path, options: Dict) -> None:
        s.level_path: Path = level_path
        s._next_path: Hero_Path = []
        s._pathes:    Pathes = []
        s.options:    Dict = options

        s.dungeon:  Dungeon | None = None
        s.hero:     Hero | None = None
        s.dragons:  List[Dragon] = []
        s.diamonds: Diamonds = {}

        s.game_over:       bool = False
        s.game_result:     Results = ""
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
        dungeon, hero, dragons, diamonds = load_levels(s.level_path)
        s.dungeon  = dungeon
        s.hero     = hero
        s.dragons  = dragons
        s.diamonds = diamonds

        s.game_over = False
        s.game_result = ""
        
        s.nb_steps = 0
        s.killed_dragons = 0
        s.shields = 2
        
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
        s.dragon_prev_mvs = [None for _ in range(len(s.dragons))]
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
        s.is_moving = False

        
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
    
    @property
    def pathes(s) -> Pathes:
        h_pos = s.hero['position']
        coords = s._next_steps(h_pos)
        
        if not coords:
            return []
        
        new_pathes = [[h_pos, crd] for crd in coords]
        return s._compute_pathes(new_pathes)
    
    @property
    def next_path(s) -> Hero_Path:
        return s._detect_priority_path()
        

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


    def _next_steps(
        s,
        pos:   Position,
        prev:  Position | None = None,
        first: bool = False
    ) -> List[Position] | None:
        stack = []
        r, c = pos
        
        for (nbr_r, nbr_c), _ in s.dungeon.neighbors(r, c):
            if prev is not None and (nbr_r, nbr_c) == prev:
                continue

            if s.dungeon.are_connected(r, c, nbr_r, nbr_c):
                if first:
                    return (nbr_r, nbr_c)
                else:
                    stack.append((nbr_r, nbr_c))

        return None if first else stack


    def _compute_pathes(s, pathes: Pathes) -> Pathes:
        new_pathes = []
        n = len(pathes)
        cntr = 0
        
        for p in pathes:
            coords = s._next_steps(p[-1], p[-2])
            
            if coords:
                new_pathes += [p + [crd] for crd in coords]
            else:
                cntr += 1
                new_pathes.append(p)
            
        if new_pathes and cntr < n:
            return s._compute_pathes(new_pathes)
        
        for i in range(n):
            pathes[i].pop(0)
        
        return pathes
         

    def _define_dragon_on_path(s, p: Hero_Path):
        path_dragons = []
        
        for crd in p:
            if s._check_diamonds(crd):
                return {'level': 100}
            
            for dragon in s.dragons:
                if dragon['position'] == crd:
                    path_dragons.append(dragon)
        
        if not path_dragons:
            return {'level': 0}
        
        path_dragons.sort(key=lambda data: data['level'])

        return path_dragons[-1]


    def _detect_priority_path(s):
        dragons_on_pathes = [
            {
                'dragon': s._define_dragon_on_path(p),
                'path': p
            } for p in s.pathes
        ]
        
        if not dragons_on_pathes:
            return dragons_on_pathes
        
        dragons_on_pathes.sort(key=lambda data: data['dragon']['level'])
        
        return dragons_on_pathes[-1]['path']


    def _detect_clash_and_winner(s, render):
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
                

    def _dragon_move(s) -> None:
        for idx, dragon in enumerate(s.dragons):
            if s.encountered_dragon is not None\
                and s.encountered_dragon == idx:
                    continue
            
            (r, c) = dragon['position']
            prev = s.dragon_prev_mvs[idx]

            dragon['position'] = s._next_steps((r, c), prev, first=True)
            if dragon['position'] is not None:
                s.dragon_prev_mvs[idx] = (r, c)
            else:
                dragon['position'] = (r, c)
                s.dragon_prev_mvs[idx] = None


    def _check_diamonds(
        s,
        pos: Position,
        delete = False
    ) -> bool:
        if not pos:
            return False
        
        for idx, diamond_pos in enumerate(s.diamonds["positions"]):
            if pos == diamond_pos:
                
                if delete:
                    del s.diamonds["positions"][idx]
                return True

        return False

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

        path = s.next_path

        for step_row, step_col in path:
            h_pos = s.hero["position"] = (step_row, step_col)
            s.walking_tick = 0
            
            is_diamond = s._check_diamonds(h_pos, delete=True)

            while s.walking_tick <= 30:
                render()
                
            if is_diamond:
                break


    def ticking(s, render):
        s.tick = (s.tick + 1) % 30
        s.dragon_tick = (s.dragon_tick + 1) % 30
        
        if not s.in_clash and not s.game_over:
            s._detect_clash_and_winner(render)
    
        if s.tick % 30 == 0 and s.options['dragons_move']:
            s._dragon_move()
        
        if s.is_moving:
            s.walking_tick += 1
        
        if s.in_clash:
            s.clash_tick += 1
