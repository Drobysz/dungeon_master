# src/view/menu_view.py
# from __future__ import annotations
from .props import *
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from game_engine.fltk import *

_THIS = Path(__file__).resolve()
_PROJECT_ROOT = _THIS.parents[3]
LEVELS_DIR = _PROJECT_ROOT / "components" / "levels"

# ------------------------------ utils -----------------------------------------
def list_levels() -> List[Path]:
    if not LEVELS_DIR.exists():
        return []
    files = [p for p in LEVELS_DIR.iterdir()
             	if p.is_file() and p.suffix.lower() == ".json"]
    files.sort(key=lambda p: p.name.lower())
    return files

def point_in_rect(x: int, y: int, r: Tuple[int, int, int, int]) -> bool:
    rx, ry, rw, rh = r
    return rx <= x <= rx + rw and ry <= y <= ry + rh

# ------------------------------ MenuView --------------------------------------
class MenuView:
	def __init__(self) -> None:
		self.levels: List[Path] = list_levels()
		self.sel: int = 0
		self.scroll: int = 0
		self.options: Dict[str, bool] = {
			"treasures": False,
			"dragons_move": False,
			"save_enabled": False,
		}
		# клик-мапа (обновляется при каждом draw)
		self.hit: Dict[str, Tuple[int, int, int, int]] = {}
		self.hit_items: List[Tuple[int, Tuple[int, int, int, int]]] = []  # (index, rect)

	# --------------------------- Rendering -------------------------------------
	def render(self) -> None:
		efface_tout()
		W, H = largeur_fenetre(), hauteur_fenetre()

		# Background
		rectangle(0, 0, W, H, remplissage=BG, couleur=BG)

		# Title
		texte(PADDING, PADDING, "WALL IS YOU — MENU", couleur=FG, taille=TITLE_SIZE)

		# Level list
		list_x = PADDING
		list_y = PADDING + TITLE_SIZE + SPACER
		list_w = max(420, int(W * 0.44))
		list_h = H - list_y - (PADDING + 160)

		# Listbox frame
		rectangle(list_x - 8, list_y - 8, list_x + list_w + 8, list_y + list_h + 8, couleur=MUTED)
		# Listbox background
		rectangle(list_x, list_y, list_x + list_w, list_y + list_h, remplissage="#14161d", couleur="#242936")

		# rendering of elements + scroll
		self.hit_items.clear()
		visible_count = max(1, list_h // LIST_ITEM_H)
		self.scroll = max(0, min(self.scroll, max(0, len(self.levels) - visible_count)))

		for vis_idx in range(visible_count):
			idx = self.scroll + vis_idx
			if idx >= len(self.levels):
				break
			item_y = list_y + vis_idx * LIST_ITEM_H
			r = (list_x, item_y, list_w, LIST_ITEM_H)
			# подложка для выбранного
			if idx == self.sel:
				rectangle(r[0], r[1], r[0]+r[2], r[1]+r[3], remplissage="#223048", couleur=ACCENT)
			# название
			fname = self.levels[idx].name.split('.')[0]
			texte(r[0] + 10, r[1] + 7, fname, couleur=FG, taille=TEXT_SIZE)
			# сохранить кликабельную область
			self.hit_items.append((idx, r))

		# buttons at the right
		right_x = list_x + list_w + PADDING
		btn_y = list_y

		self.hit["btn_play"] = (right_x, btn_y, BTN_W, BTN_H)
		self._button(self.hit["btn_play"], "Play", primary=True)

		btn_y += BTN_H + SPACER
		self.hit["btn_quit"] = (right_x, btn_y, BTN_W, BTN_H)
		self._button(self.hit["btn_quit"], "Exit", danger=True)

		# options (checkboxes)
		opt_y = btn_y + BTN_H + SPACER * 3
		texte(right_x, opt_y - 10, "Options:", couleur=FG, taille=TEXT_SIZE)
		opt_y += SPACER * 1.5
  
		keys = ["treasures", "dragons_move", "save_enabled"]
		names = ["Treasures", "Dragon moves", "Saving"]
  
		for id in range(len(keys)):
			opt_key = "opt_" + keys[id]
			key = keys[id]	
 
			self.hit[opt_key] = (right_x, opt_y, 22, 22)
			self._checkbox(self.hit[opt_key], self.options[key])
			texte(right_x + 30, opt_y - 3, names[id], couleur=FG, taille=TEXT_SIZE)
			opt_y += CHECK_H + 6

		# control hints
		hint = (
			"↑/↓ — choose level   Enter — play   Q — exit\n"
			"LMC — choose/activate option   PgUp/PgDn — scrolling\n"
			"Control in the game:\n"
   			"  LMC — cell rotation, Space — move\n"
   			"  R — restart, Esc — menu\n"
		)
		texte(PADDING, H - 2*PADDING - 4*HINT_SIZE, hint, couleur=MUTED, taille=HINT_SIZE)
	
	def reload(self):
		self.render()
		mise_a_jour()

	# Button
	def _button(self, r: Tuple[int,int,int,int], label: str, primary=False, danger=False) -> None:
		x, y, w, h = r
		color = "#243145"
		border = ACCENT if primary else (DANGER if danger else "#3a4050")
		fill = "#1b2230" if not primary else "#29405f"
		if danger:
			fill = "#3c1e1e"
		rectangle(x, y, x+w, y+h, remplissage=fill, couleur=border)
		texte(x + 14, y + 10, label, couleur=FG, taille=TEXT_SIZE)

	# Checkbox
	def _checkbox(self, r: Tuple[int,int,int,int], checked: bool) -> None:
		x, y, w, h = r
		rectangle(x, y, x+w, y+h, remplissage="#10141b", couleur="#3a4050")
		if checked:
			# cross
			ligne(x+4, y+13, x+10, y+h-5, couleur=OK, epaisseur=3)
			ligne(x+10, y+h-5, x+w-5, y+5, couleur=OK, epaisseur=3)

	# --------------------------- Event handler ----------------------------------------
	def handle_event(self, ev, et) -> Optional[Dict]:
		"""
		Возвращает:
		- {"action":"start","level":Path,"options":{...}}
		- {"action":"quit"}
		- None — если решений пока нет
		"""
		if et is None:
			return None

		if et == "Touche":			
			key = touche(ev)

			match key:
				case "Up" | "KP_Up":
					self._move_sel(-1)
				case "Down" | "KP_Down":
					self._move_sel(1)
				case "Prior":
					self._move_sel(-5)
				case "Next":
					self._move_sel(+5)
				case "Return" | "space":
					if self._has_selection():
						return {
          					"action": "start",
               				"level": self.levels[self.sel],
                   			"options": dict(self.options)
                      	}
				case "q" | "Q" | "Escape":
						return {"action": "quit"}

			self.reload()
			return None

		if et == "ClicGauche":
			x, y = abscisse(ev), ordonnee(ev)

			# click on list elements
			for idx, r in self.hit_items:
				if point_in_rect(x, y, r):
					self.sel = idx
					self._ensure_sel_visible()
					self.reload()
					return None

		# clock on buttons
		if "btn_play" in self.hit and point_in_rect(x, y, self.hit["btn_play"]):
			if self._has_selection():
				return {
					"action": "start",
					"level": self.levels[self.sel],
					"options": dict(self.options)
				}
		if "btn_quit" in self.hit and point_in_rect(x, y, self.hit["btn_quit"]):
			return {"action": "quit"}

		# click on checkboxes
		for key in ("opt_treasures", "opt_dragons_move", "opt_save_enabled"):
			r = self.hit.get(key)
			if r and point_in_rect(x, y, r):
				self._toggle_option(key)
				return None
  
		return None

	# --------------------------- helpers --------------------------------
	def _toggle_option(self, key: str) -> None:
		match key:
			case "opt_treasures":
				self.options["treasures"] = not self.options["treasures"]
			case "opt_dragons_move":
				self.options["dragons_move"] = not self.options["dragons_move"]
			case "opt_save_enabled":
				self.options["save_enabled"] = not self.options["save_enabled"]

		self.reload()

	def _has_selection(self) -> bool:
		return 0 <= self.sel < len(self.levels)

	def _move_sel(self, shift: int) -> None:
		if not self.levels:
			self.sel = 0
			return
		self.sel = max(0, min(len(self.levels) - 1, self.sel + shift))
		self._ensure_sel_visible()

	def _ensure_sel_visible(self) -> None:
		# держим выбранный элемент в видимой зоне
		if not self.levels:
			self.scroll = 0
			return
		H = hauteur_fenetre()
		list_y = PADDING + TITLE_SIZE + SPACER
		list_h = H - list_y - (PADDING + 160)
		visible = max(1, list_h // LIST_ITEM_H)

		if self.sel < self.scroll:
			self.scroll = self.sel
		elif self.sel >= self.scroll + visible:
			self.scroll = self.sel - visible + 1
		self.scroll = max(0, min(self.scroll, max(0, len(self.levels) - visible)))