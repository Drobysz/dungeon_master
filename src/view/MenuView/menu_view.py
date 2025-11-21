from .props import *
from .classes import *
from pathlib import Path
from typing import Dict, List, Optional
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

def point_in_rect(x: int, y: int, r: Coord) -> bool:
    rx, ry, rw, rh = r
    return rx <= x <= rx + rw and ry <= y <= ry + rh

# ------------------------------ MenuView --------------------------------------
class MenuView:
	def __init__(self) -> None:
		self.levels:    List[Path] = list_levels()
		self.sel:       int = 0
		self.scroll:    int = 0
		self.options:   GameProps = {
			"treasures": False,
			"dragons_move": False,
			"save_enabled": False,
		}
		self.hit:       Hitbox = {}
		self.hit_items: ListHitBox = []

	# --------------------------- Rendering -------------------------------------
	def render(self) -> None:
		efface_tout()
		W, H = largeur_fenetre(), hauteur_fenetre()

		# Background
		rectangle(0, 0, W, H, remplissage=BG, couleur=BG)

		# Title
		texte(
      		PADDING, PADDING,
        	"WALL IS YOU — MENU",
         	couleur=FG,
          	taille=TITLE_SIZE
        )

		# Level list
		list_x = PADDING
		list_y = PADDING + TITLE_SIZE + SPACER
		list_w = max(420, int(W * 0.44))
		list_h = H - list_y - (PADDING + 160)

		# Listbox frame
		rectangle(
      		list_x - 8,
        	list_y - 8,
         	list_x + list_w + 8,
          	list_y + list_h + 8,
           	couleur=MUTED
        )

		# Listbox background
		rectangle(
      		list_x, list_y,
        	list_x + list_w,
         	list_y + list_h,
          	remplissage="#14161d",
           	couleur="#242936"
        )

		# rendering of levels + scroll
		self.hit_items.clear()
		visible_count = max(1, list_h // LIST_ITEM_H)
		ln_lvls = len(self.levels)
  
		out = max(0, ln_lvls - visible_count)
		self.scroll = max(0, min(self.scroll, out))

		for vis_idx in range(visible_count):
			idx = self.scroll + vis_idx
			if idx >= ln_lvls:
				break
			item_y = list_y + vis_idx * LIST_ITEM_H
			r = (list_x, item_y, list_w, LIST_ITEM_H)
			# the background for the selected
			if idx == self.sel:
				rectangle(
        			r[0], r[1],
           			r[0]+r[2], r[1]+r[3],
              		remplissage="#223048",
                	couleur=ACCENT
                )
			# name
			fname = self.levels[idx].name.split('.')[0]
			texte(
       			r[0] + 10, r[1] + 7,
          		fname,
            	couleur=FG,
             	taille=TEXT_SIZE
            )
			# save hitbox area
			self.hit_items.append((idx, r))

		# buttons at the right
		right_x = list_x + list_w + PADDING
		btn_y = list_y

		self.hit["btn_play"] = (right_x, btn_y, BTN_W, BTN_H)
		self._button(self.hit["btn_play"], "Play", props="primary")

		btn_y += BTN_H + SPACER
		self.hit["btn_quit"] = (right_x, btn_y, BTN_W, BTN_H)
		self._button(self.hit["btn_quit"], "Exit", props="danger")

		# options (checkboxes)
		opt_y = btn_y + BTN_H + SPACER * 3
		texte(right_x, opt_y - 10, "Options:", couleur=FG, taille=TEXT_SIZE)
		opt_y += SPACER * 1.5
  
		keys  = ["treasures", "dragons_move", "save_enabled"]
		names = ["Treasures", "Dragon moves", "Saving"]
  
		for id in range(len(keys)):
			opt_key = "opt_" + keys[id]
			key = keys[id]	
 
			self.hit[opt_key] = (right_x, opt_y, 22, 22)
			self._checkbox(self.hit[opt_key], self.options[key])
			texte(
       			right_x + 30, opt_y - 3,
          		names[id],
            	couleur=FG,
             	taille=TEXT_SIZE
            )
			opt_y += CHECK_H + 6

		# control hints
		hint = (
			"↑/↓ — choose level   Enter — play   Q — exit\n"
			"LMB — choose/activate option   PgUp/PgDn — scrolling\n"
			"Control in the game:\n"
   			"  LMB — cell rotation, Space — move\n"
   			"  R — restart, Esc — menu\n"
		)
		texte(PADDING, H - 2 * PADDING - 4 * HINT_SIZE, hint, couleur=MUTED, taille=HINT_SIZE)

		mise_a_jour()

	# --------------------------- Components -------------------------------------
	# Button
	def _button(
    	self,
     	r: Coord,
      	label: str,
        props: BtnTypes = "default"
    ) -> None:
		match props:
			case "primary":
				border = ACCENT
				fill = "#29405f"
			case "danger":
				border = DANGER
				fill = "#3c1e1e"
			case _:
				border = "#3a4050"
				fill = "#1b2230"
    
		x, y, w, h = r
    
		rectangle(
      		x, y,
        	x+w, y+h,
         	remplissage=fill,
          	couleur=border
        )
  
		texte(x + 14, y + 10, label, couleur=FG, taille=TEXT_SIZE)

	# Checkbox
	def _checkbox(self, r: Coord, checked: bool) -> None:
		x, y, w, h = r
		rectangle(
      		x, y,
        	x+w, y+h,
         	remplissage="#10141b",
          	couleur="#3a4050"
        )
		if checked:
			# cross
			ligne(x+4, y+13, x+10, y+h-5, couleur=OK, epaisseur=3)
			ligne(x+10, y+h-5, x+w-5, y+5, couleur=OK, epaisseur=3)

	# --------------------------- Event handler ----------------------------------------
	def handle_event(s, ev, et) -> Optional[Dict]:
		if et is None:
			return None

		if et == "Touche":			
			key = touche(ev)

			match key:
				case "Up" | "KP_Up":
					s._move_sel(-1)
				case "Down" | "KP_Down":
					s._move_sel(1)
				case "Prior":
					s._move_sel(-5)
				case "Next":
					s._move_sel(+5)
				case "Return" | "space":
					if s._has_selection():
						return {
          					"action": "start",
               				"level": s.levels[s.sel],
                   			"options": dict(s.options)
                      	}
				case "q" | "Q" | "Escape":
						return {"action": "quit"}

			s.render()
			return None

		if et == "ClicGauche":
			x, y = abscisse(ev), ordonnee(ev)

			# click on list elements
			for idx, r in s.hit_items:
				if point_in_rect(x, y, r):
					s.sel = idx
					s._ensure_sel_visible()
					s.render()
					return None

			# clock on buttons
			if "btn_play" in s.hit and point_in_rect(x, y, s.hit["btn_play"]):
				if s._has_selection():
					return {
						"action": "start",
						"level": s.levels[s.sel],
						"options": dict(s.options)
					}
			if "btn_quit" in s.hit and point_in_rect(x, y, s.hit["btn_quit"]):
				return {"action": "quit"}

			# click on checkboxes
			for opt in ("opt_treasures", "opt_dragons_move", "opt_save_enabled"):
				r = s.hit.get(opt)
				if r and point_in_rect(x, y, r):
					s._toggle_option(opt)
					return None
  
		return None

	# --------------------------- helpers --------------------------------
	def _toggle_option(s, key: str) -> None:
		opt = s.options[key[4:]]
		s.options[key[4:]] = not opt
		s.render()
	
	def _has_selection(s) -> bool:
		return 0 <= s.sel < len(s.levels)

	def _move_sel(s, shift: int) -> None:
		if not s.levels:
			s.sel = 0
			return
		s.sel = max(0, min(len(s.levels) - 1, s.sel + shift))
		s._ensure_sel_visible()

	def _ensure_sel_visible(s) -> None:
		# держим выбранный элемент в видимой зоне
		if not s.levels:
			s.scroll = 0
			return
		H = hauteur_fenetre()
		list_y = PADDING + TITLE_SIZE + SPACER
		list_h = H - list_y - (PADDING + 160)
		visible = max(1, list_h // LIST_ITEM_H)

		if s.sel < s.scroll:
			s.scroll = s.sel
		elif s.sel >= s.scroll + visible:
			s.scroll = s.sel - visible + 1
		s.scroll = max(0, min(s.scroll, max(0, len(s.levels) - visible)))