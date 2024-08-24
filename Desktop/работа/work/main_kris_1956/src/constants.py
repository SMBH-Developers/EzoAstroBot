from pathlib import Path

__all__ = ['DATA_DIR', 'SESSIONS_DIR', 'FILES_DIR', 'LOGS_DIR', 'IGNORE_LIST', 'BASE_DIR']


BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / "data"

SESSIONS_DIR = DATA_DIR / "sessions"
FILES_DIR = DATA_DIR / "files"
LOGS_DIR = DATA_DIR / "logs"

IGNORE_LIST = DATA_DIR / "ignore_list.json"
