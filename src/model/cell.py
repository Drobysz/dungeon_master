class Cell:
    north: bool; east: bool; south: bool; west: bool
    
    def rotate(self) -> "Cell":
        return Cell(
            north = self.west,
            east = self.north,
            south = self.east,
            west = self.south
        )
        
    def has_dir(self, dir: str) -> bool:
        return {
            "N": self.north,
            "E": self.east,
            "S": self.south,
            "W": self.west
        }[dir]