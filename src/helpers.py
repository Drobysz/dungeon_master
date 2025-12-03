from pathlib import Path
from typing import List

def get_filename(p: Path) -> str:
    return p.name.split('.')[0]


_THIS = Path(__file__).resolve()
_PROJECT_ROOT = _THIS.parents[1]
LEVELS_DIR = _PROJECT_ROOT / "levels"

def list_levels() -> List[Path]:
    if not LEVELS_DIR.exists():
        return []
    files = [p for p in LEVELS_DIR.iterdir()
             	if p.is_file() and p.suffix.lower() == ".json"]
    files.sort(key=lambda p: p.name.lower())
    return files