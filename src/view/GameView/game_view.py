from typing import Optional, Tuple, List
from .classes import Position
from .props import *
from model.dungeon import Dungeon

from game_engine.fltk import *

from controller.game_controller import GameController

class GameView:
    def __init__(self, controller: GameController, cell_size: int = 64, margin: int = 40) -> None:
        self.controller = controller
        self.cell_size = cell_size
        self.margin_x = margin
        self.margin_y = margin

    # ------------------------ coordinate utilities ------------------------

    def _grid_to_pixel(self, row: int, col: int) -> Tuple[int, int]:
        x = self.margin_x + col * self.cell_size
        y = self.margin_y + row * self.cell_size
        return x, y

    def _grid_center(self, row: int, col: int) -> Tuple[int, int]:
        x, y = self._grid_to_pixel(row, col)
        x += self.cell_size // 2
        y += self.cell_size // 2
        return x, y

    def _pixel_to_grid(self, x: int, y: int) -> Optional[Position]:
        dungeon = self.controller.dungeon
        if dungeon is None:
            return None

        grid_x = x - self.margin_x
        grid_y = y - self.margin_y
        if grid_x < 0 or grid_y < 0:
            return None

        col = grid_x // self.cell_size
        row = grid_y // self.cell_size

        if not dungeon.in_bound(row, col):
            return None

        return row, col

    # --------------------------- rendering ---------------------------

    def render(self) -> None:
        efface_tout()

        width = largeur_fenetre()
        height = hauteur_fenetre()

        # background
        rectangle(0, 0, width, height, remplissage=BACKGROUND, couleur=BACKGROUND)

        dungeon = self.controller.dungeon
        if dungeon is None:
            texte(20, 20, "No loaded level", couleur=TEXT_COLOR, taille=20)
            return

        # frame under field
        grid_width = dungeon.w * self.cell_size
        grid_height = dungeon.h * self.cell_size
        rectangle(
            self.margin_x - 6,
            self.margin_y - 6,
            self.margin_x + grid_width + 6,
            self.margin_y + grid_height + 6,
            couleur=GRID_BORDER,
        )
        rectangle(
            self.margin_x,
            self.margin_y,
            self.margin_x + grid_width,
            self.margin_y + grid_height,
            remplissage=GRID_BG,
            couleur=GRID_BORDER,
        )

        # cells
        self._render_grid(dungeon)

        # intention path
        self._render_path()

        # entities
        self._render_entities()

        # HUD
        self._render_hud()

        # Game Over overlay
        if self.controller.game_over:
            self._render_game_over_overlay()

        mise_a_jour()

    def _render_grid(self, dungeon: Dungeon) -> None:
        gap = 8  # distance between cells, in pixels

        # actual size of the drawn cell (smaller than the logical cell_size)
        tile_size = self.cell_size - gap
        half_tile = tile_size // 2

        # length of the door segment along the side of the cage
        door_length = int(tile_size * 0.6)
        half_door = door_length // 2

        for row in range(dungeon.h):
            for col in range(dungeon.w):
                # logical upper left corner of the cell
                base_x = self.margin_x + col * self.cell_size
                base_y = self.margin_y + row * self.cell_size

                # internal (visible) cell with indents on all sides
                x = base_x + gap // 2
                y = base_y + gap // 2

                left_x = x
                right_x = x + tile_size
                top_y = y
                bottom_y = y + tile_size

                # specific cell frame
                rectangle(left_x, top_y, right_x, bottom_y, couleur=CELL_BORDER)

                cell = dungeon.get_cell(row, col)

                # upper edge (North)
                if cell.north:
                    x1 = x + half_tile - half_door
                    x2 = x + half_tile + half_door
                    y_edge = top_y
                    ligne(x1, y_edge, x2, y_edge, couleur=CELL_DOOR, epaisseur=3)

                # lower edge (South)
                if cell.south:
                    x1 = x + half_tile - half_door
                    x2 = x + half_tile + half_door
                    y_edge = bottom_y
                    ligne(x1, y_edge, x2, y_edge, couleur=CELL_DOOR, epaisseur=3)

                # left edge (West)
                if cell.west:
                    y1 = y + half_tile - half_door
                    y2 = y + half_tile + half_door
                    x_edge = left_x
                    ligne(x_edge, y1, x_edge, y2, couleur=CELL_DOOR, epaisseur=3)

                # right edge (East)
                if cell.east:
                    y1 = y + half_tile - half_door
                    y2 = y + half_tile + half_door
                    x_edge = right_x
                    ligne(x_edge, y1, x_edge, y2, couleur=CELL_DOOR, epaisseur=3)

    def _render_level(self, lvl, x, y, radius):
        padding = 10
        font_size = max(10, radius)
        if lvl < 10:
            padding /= 2
        texte(x - padding, y - 10, str(lvl), couleur='yellow', taille=font_size)

    def _render_entities(self) -> None:
        for dragon in self.controller.dragons:
            row, col = dragon["position"]
            x, y = self._grid_center(row, col)
            radius = self.cell_size // 3
            cercle(x, y, radius, remplissage=DRAGON_COLOR, couleur=DRAGON_COLOR)
        
            # dragon level
            self._render_level(dragon["level"], x, y, radius)
            
        hero = self.controller.hero
        if hero is not None:
            row, col = hero["position"]
            x, y = self._grid_center(row, col)
            radius = self.cell_size // 3
            cercle(x, y, radius, remplissage=HERO_COLOR, couleur=HERO_COLOR)
        
            # hero level
            self._render_level(hero["level"], x, y, radius)

    def _render_path(self) -> None:
        path: List[Position] = self.controller.last_path
        hero = self.controller.hero

        if not path or hero is None:
            return

        points: List[Tuple[int, int]] = []
        start_row, start_col = hero["position"]
        points.append(self._grid_center(start_row, start_col))

        for row, col in path:
            points.append(self._grid_center(row, col))

        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            ligne(x1, y1, x2, y2, couleur=PATH_COLOR, epaisseur=3)

    def _render_hud(self) -> None:
        height = hauteur_fenetre()

        hero = self.controller.hero
        hero_level = hero["level"] if hero is not None else "?"

        dragons_count = len(self.controller.dragons)

        controls = "LMB — rotate cell   Space — move   R — reset   Esc — menu"
        texte(20, height - 60, controls, couleur=MUTED_COLOR, taille=16)

        info = f"Hero level: {hero_level}   Dragons: {dragons_count}"
        texte(20, height - 35, info, couleur=TEXT_COLOR, taille=18)

    def _render_game_over_overlay(self) -> None:
        width = largeur_fenetre()
        height = hauteur_fenetre()

        # translucent rectangle
        rectangle(0, 0, width, height, remplissage=OVERLAY_BG, couleur=OVERLAY_BG)

        result = self.controller.game_result
        if result == "win":
            msg = "Win! All dragons are defeated."
        elif result == "lose":
            msg = "Defeat. The hero died."
        else:
            msg = "Game Over."

        texte(width // 2 - 150, height // 2 - 20, msg, couleur=TEXT_COLOR, taille=24)
        texte(
            width // 2 - 100,
            height // 2 + 20,
            "Enter — restart   Esc — menu",
            couleur=MUTED_COLOR,
            taille=18,
        )

    # ------------------------- event handler -------------------------

    def handle_event(self, ev, ev_type: str):
        if ev_type is None:
            return None

        if ev_type == "Touche":
            key = touche(ev)

            if self.controller.game_over:
                match key:
                    case "Return" | "space" | "r" | "R":
                        return "RESTART"
                    case "Escape":
                        return "TO_MENU"
                return None

            match key:
                case "space":
                    return "END_TURN"
                case "r" | "R":
                    self.controller.reset()
                    return "RESTART"
                case "Escape":
                    return "TO_MENU"

            return None

        if ev_type == "ClicGauche":
            x = abscisse(ev)
            y = ordonnee(ev)

            grid_pos = self._pixel_to_grid(x, y)
            if grid_pos is not None:
                row, col = grid_pos
                self.controller.rotate_cell(row, col)
        
        self.render()
        return None