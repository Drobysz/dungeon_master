from typing import List, Tuple, Literal

Animations = Literal["attack", "shield", "walk", "none"]
Results =    Literal["win", "lose", ""]
Position =   Tuple[int, int]
Hero_Path =  List[Position]
Pathes =     List[Hero_Path]