from typing import Dict, List, Literal, Tuple

Coord = Tuple[int, int, int, int]
Hitbox = Dict[str, Coord]
ListHitBox = List[Tuple[int, Coord]]
GameProps = Dict[str, bool]
BtnTypes = Literal["primary", "danger", "default"]