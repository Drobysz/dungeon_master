from dataclasses import dataclass
from .cell import Cell
from typing import List, Iterable, Tuple, Literal, Dict

Grid = List[List[Cell]]
Position = Tuple[int, int]
Dir = Literal["N", "E", "S", "W"]
Dirs = Dict[Dir, Position]
OppDirs = Dict[Dir, Dir]

DIRECTIONS: Dirs = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}
OPPOSITE: OppDirs = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E"
}

@dataclass
class Dungeon:
	grid: Grid

	@property
	def h(s) -> int: return len(s.grid)
	@property
	def w(s) -> int: return len(s.grid[0])

	def get_cell(s, r: int, c: int) -> Cell:
		return s.grid[r][c]

	def rotate_cell(s, r: int, c: int) -> None:
		cell = s.grid[r][c]
		cell = cell.rotate()

	def in_bound(s, r: int, c: int) -> bool:
		return 0 <= r <= s.h and 0 <= c <= s.w

	def neighbors(s, r: int, c: int) -> Iterable[Tuple[Position, str]]:
		for dir, (r_shift, c_shift) in DIRECTIONS.items():
			n_r = r + r_shift
			n_c = c + c_shift
			if s.in_bound(n_r, n_c):
				yield (n_r, n_c), dir
    
	def are_connected(
		self,

		row: int,
		col: int,

		n_row: int,
		n_col: int
	) -> bool:
		shifted_row = n_row - row
		shifted_col = n_col - col
  
		for direction, (shift_row, shift_col) in DIRECTIONS.items():
			if (shifted_row, shifted_col) == (shift_row, shift_col):
				cell = self.get_cell(row, col)
				n_cell = self.get_cell(n_row, n_cell)
				return cell.has_dir(direction) and n_cell.has_dir(OPPOSITE[direction])