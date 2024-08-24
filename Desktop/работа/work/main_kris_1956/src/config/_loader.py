import json
from pyrogram import Client

from src.config import settings
from src.constants import SESSIONS_DIR, IGNORE_LIST

from . import _logger_config


__all__ = ["client", "ignore_ls"]


client = Client(name=f'{SESSIONS_DIR / settings.name}', api_id=settings.api_id, api_hash=settings.api_hash, phone_number=settings.phone)

for _json_file in [IGNORE_LIST]:
    if not _json_file.exists():
        _json_file.write_text('[]')

ignore_ls = json.loads(IGNORE_LIST.read_text())

_logger_config.init()
