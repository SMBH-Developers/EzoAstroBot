import json
import asyncio

from pyrogram import Client

from src.config import settings
from src.constants import SESSIONS_DIR


client = Client(name=f'{SESSIONS_DIR / settings.name}', api_id=settings.api_id, api_hash=settings.api_hash, phone_number=settings.phone)
ls = []


async def check_dialogs():
    async with client:
        count = 0
        try:
            async for dialog in client.get_dialogs():
                if dialog.chat.id > 0:
                    ls.append(dialog.chat.id)
                    count += 1
                    print(count)
        finally:
            with open('data/ignore_list.json', 'w') as f:
                json.dump(ls, f)


asyncio.run(check_dialogs())
