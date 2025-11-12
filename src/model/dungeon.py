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
	def height(self) -> int: return len(self.grid)
	@property
	def width(self) -> int: return len(self.grid[0])

	def get_cell(self, row: int, col: int) -> Cell:
		return self.grid[row][col]

	def rotate_cell(self, row: int, col: int) -> None:
		cell = self.grid[row][col]
		cell = cell.rotate()

	def in_bound(self, row: int, col: int) -> bool:
		return 0 <= row <= self.height and 0 <= col <= self.width

	def neighbors(self, row: int, col: int) -> Iterable[Tuple[Position, str]]:
		for dir, (r_shift, c_shift) in DIRECTIONS.items():
			n_row = row + r_shift
			n_col = col + c_shift
			if self.in_bound(n_row, n_col):
				yield (n_row, n_col), dir
    
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
			if  (shifted_row, shifted_col) == (shift_row, shift_col):
				cell = self.get_cell(row, col)
				n_cell = self.get_cell(n_row, n_cell)
				return cell.has_dir(direction) and n_cell.has_dir(OPPOSITE[direction])