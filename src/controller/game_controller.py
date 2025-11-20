from __future__ import annotations
from typing import Dict, List, Tuple, Literal
from pathlib import Path

from load_levels import load_levels
from model.dungeon import Dungeon

Position = Tuple[int, int]
Entity = Dict[int, List[int, int]]


class GameController:
    """
    Отвечает за состояние игры:
    - поле (Dungeon)
    - герой
    - драконы
    - опции (treasures / dragons_move / save и т.п.)
    """

    def __init__(self, level_path: Path, options: Dict) -> None:
        self.level_path: Path = level_path
        self.options: Dict = options

        self.dungeon: Dungeon | None = None
        self.hero: Entity | None = None
        self.dragons: List[Dict] = []

        self.game_over: bool = False
        self.game_result: Literal["win", "lose", ""] = ""

        self._load_level()

    # -------------------- загрузка / сброс уровня --------------------

    def _load_level(self) -> None:
        """Читает json и наполняет dungeon/hero/dragons."""
        dungeon, hero, dragons = load_levels(self.level_path)
        self.dungeon = dungeon
        self.hero = hero
        self.dragons = dragons
        self.game_over = False
        self.game_result = ""

    def reset(self) -> None:
        """Перезапустить тот же уровень с нуля."""
        self._load_level()

    # -------------------- работа с полем --------------------

    def rotate_cell(self, row: int, col: int) -> None:
        if self.dungeon is None:
            return

        if not self.dungeon.in_bounds(row, col):
            return

        self.dungeon.rotate_cell(row, col)

    # пример: поворот по координатам пикселей, когда будет GameView
    def rotate_cell_from_pixel(self, x: int, y: int, cell_size: int) -> None:
        """
        Переводит пиксели (x, y) в индекс клетки и вызывает rotate_cell.
        Удобно использовать в обработчике клика мышью.
        """
        row = y // cell_size
        col = x // cell_size
        self.rotate_cell(row, col)

    # -------------------- ход / логика игры --------------------

    def end_turn(self) -> None:
        """
        Заготовка под ход героя:
        - построить «намерение»
        - сделать шаг
        - проверить встречи с драконами
        - проставить game_over / game_result
        Сейчас пустая, заполним на 5-й день.
        """
        if self.game_over or self.dungeon is None or self.hero is None:
            return

        # TODO: логика хода героя и боёв
        pass

    def is_over(self) -> bool:
        return self.game_over