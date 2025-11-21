class Cell: 
    def __init__(self, n, e, s, w):
        self.north: bool = n
        self.east: bool = e
        self.south: bool = s
        self.west: bool = w
    
    def rotate(s) -> "Cell":
        return Cell(
            n = s.west,
            e = s.north,
            s = s.east,
            w = s.south
        )
        
    def has_dir(s, dir: str) -> bool:
        return {
            "N": s.north,
            "E": s.east,
            "S": s.south,
            "W": s.west
        }[dir]