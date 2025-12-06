from pathlib import Path
from typing import List

def get_filename(p: Path) -> str:
    return p.name.split('.')[0]


_THIS = Path(__file__).resolve()
_PROJECT_ROOT = _THIS.parents[1]

def get_complete_path(PATH):
    return _PROJECT_ROOT / PATH

def list_files(path = "levels", ext = "json") -> List[Path]:
    LEVELS_DIR = _PROJECT_ROOT / path

    if not LEVELS_DIR.exists():
        return []
    files = [p for p in LEVELS_DIR.iterdir()
             	if p.is_file() and p.suffix.lower() == "." + ext]
    files.sort(key=lambda p: p.name.lower())
    return files