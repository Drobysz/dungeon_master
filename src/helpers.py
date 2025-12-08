from pathlib import Path
from typing import List, Dict

_THIS = Path(__file__).resolve()
_PROJECT_ROOT = _THIS.parents[1]

Map = List[List[Dict[str, bool]]]

symbols = {
    '╬': { "top": True, "right": True, "bottom": True, "left": True},
    
    '╠': { "top": True, "right": True, "bottom": True, "left": False},
    '╣': { "top": True, "right": False, "bottom": True, "left": True},
    '╦': { "top": False, "right": True, "bottom": True, "left": True},
    '╩': { "top": True, "right": True, "bottom": False, "left": True},
    
    '═': { "top": False, "right": True, "bottom": False, "left": True},
    '║': { "top": True, "right": False, "bottom": True, "left": False},
    '╔': { "top": False, "right": True, "bottom": True, "left": False},
    '╗': { "top": False, "right": False, "bottom": True, "left": True},
    '╚': { "top": True, "right": True, "bottom": False, "left": False},
    '╝': { "top": True, "right": False, "bottom": False, "left": True},
    
    '╥': { "top": False, "right": False, "bottom": True, "left": False},
    '╨': { "top": True, "right": False, "bottom": False, "left": False},
    '╡': { "top": False, "right": False, "bottom": False, "left": True},
    '╞': { "top": False, "right": True, "bottom": False, "left": False}
}


def get_filename(p: Path) -> str:
    return p.name.split('.')[0]


def get_complete_path(PATH) -> Path:
    return _PROJECT_ROOT / PATH


def list_files(path = "levels", ext = "json") -> List[Path]:
    LEVELS_DIR = get_complete_path(path)

    if not LEVELS_DIR.exists():
        return []
    files = [p for p in LEVELS_DIR.iterdir()
             	if p.is_file() and p.suffix.lower() == "." + ext]
    files.sort(key=lambda p: p.name.lower())
    return files


def get_content_from_file(path: Path) -> str:
    f = open(path, 'r')
    content = f.read()
    f.close()
    
    return content


def convert_map(path: Path) -> Map:
    map: Map = []
    content = get_content_from_file(path)
    ln = len(content)
    i = 0
    
    while i < ln:
        row = []
        
        while i < ln and content[i] != '\n':
            cell = symbols[content[i]]
            row.append(cell)
            i += 1

        map.append(row)
        i += 1
    
    return map
    