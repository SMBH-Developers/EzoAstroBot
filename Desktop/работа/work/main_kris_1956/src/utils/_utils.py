import asyncio
from datetime import datetime
from typing import List, Sequence

from pyrogram import errors
from loguru import logger
from sqlalchemy import Row

from src.models.db import FunnelUser
from src.dispatcher.types import MyGeneratedMessage
from src.funnels import funnels


async def gather_tasks_buffer(tasks: List[asyncio.Task], *, ignore_length: bool = False):
    if len(tasks) >= 25 or ignore_length:
        await _gather_tasks(tasks)
        tasks.clear()


async def _gather_tasks(tasks: List):
    results = await asyncio.gather(*tasks, return_exceptions=True)
    exceptions = [ex for ex in results if isinstance(ex, Exception)]
    if len(exceptions) > 0:
        print(f'{len(exceptions)=}')
    try:
        with logger.catch(level="DEBUG"):
            for exception in exceptions:
                if not isinstance(exception, (errors.PeerIdInvalid, errors.InputUserDeactivated)):
                    raise exception
    except:
        pass


async def _get_user_funnel_message(id_: int, day: str, step: str | int, funnel: str) -> MyGeneratedMessage | None:
    # noinspection PyPep8Naming
    FunnelConfig = funnels[funnel]
    if day in FunnelConfig.config.days:
        messages = (await FunnelConfig.get_message(id_, day))[int(step):]
        if messages:
            return messages[0]


async def should_get_message(user: Row[int, datetime, str, datetime, datetime | None, str]):
    day, step = user.step.split('-')
    message = await _get_user_funnel_message(user.id, day, int(step), user.funnel)
    if message is None:
        # logger.error(f'SYSTEM | [{user.id}] Empty list of messages. step: {day}-{step}')
        return True  # TODO normal
    return await message.filter(user.id, day, step,
                                funnel_timestamp=user.funnel_timestamp,
                                bot_reply=user.last_message_at_bot, user_reply=user.last_message_at_user)


async def filter_users(users: Sequence[FunnelUser]) -> Sequence[FunnelUser]:
    """
    Filter users by funnel skip days and time
    :param users: [id, registration_date, step (e.g. 0-0), funnel]
    """
    users = [user for user in users if (
        (datetime.now() - user.funnel_timestamp).total_seconds() > (int(user.step.split('-')[0]) * 24 * 60 * 60)
    )]

    users = [user for user in users if await should_get_message(user)]

    return users
