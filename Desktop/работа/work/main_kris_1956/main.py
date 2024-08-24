import json
import asyncio
from asyncio import Task
from typing import List

from pyrogram import Client, types, filters
from loguru import logger

from src.config import client, ignore_ls
from src.constants import IGNORE_LIST
from src.models import db
from src import utils
from src.utils import funnel_utils
from src.dispatcher import Dispatcher


ADMIN_IDS = [1188441997, 791363343, 801831166]


@client.on_message((filters.chat('me') | filters.chat(ADMIN_IDS)) & filters.command('users_today'))
async def send_users_today(_, message: types.Message):
    await client.send_message(message.chat.id, f'Пользователей за сегодня: {await db.get_count_users_today()}')


@client.on_message(filters.private & ~filters.me & ~filters.bot)
async def get_messages_from_users(_: Client, message: types.Message):
    """Регистрация пользователя"""
    if message.from_user.id not in ignore_ls and not await db.check_user_exists(message.from_user.id):
        await db.registrate_if_not_exists(message.from_user.id)


@client.on_message(filters.private & ~filters.me & ~filters.bot, group=1)
async def update_last_user_message(_, message: types.Message):
    if await db.check_user_exists(message.from_user.id):
        await db.update_last_message_at_user(message.from_user.id)


async def sending_to_users():
    """Отправка сообщений пользователям"""
    tasks: List[Task] = []

    while True:
        try:
            print('i work')
            users = await db.get_users_by_status()
            users = await utils.filter_users(users)  # # IT'S NOT LIST OF INTEGERS (IDS)

            for user in users:
                await asyncio.sleep(0.1)
                tasks.append(asyncio.create_task(Dispatcher().dispatch_funnel_day(user.id)))
                await utils.gather_tasks_buffer(tasks)

            await utils.gather_tasks_buffer(tasks, ignore_length=True)
        except:
            logger.opt(exception=True).critical("Crash inside main while True <sending_to_users>")
        finally:
            print('Жду 15 секунд...')
            await asyncio.sleep(15)


async def main():
    await client.start()
    await sending_to_users()


def on_shutdown():
    if client.is_connected:
        client.stop()

    with IGNORE_LIST.open('w') as f:
        json.dump(ignore_ls, f, ensure_ascii=False, indent=4)
    logger.critical("Bot is stopped")


if __name__ == "__main__":
    try:
        client.run(main())
    finally:
        on_shutdown()
