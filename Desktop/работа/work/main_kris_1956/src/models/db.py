from datetime import date, datetime, timedelta

from sqlalchemy import select, update, func, Row
from loguru import logger

from ._engine import async_session
from ._models import *


FunnelUser = Row[int, datetime, str, str, datetime, datetime | None]


async def registrate_if_not_exists(id_: int):
    async with async_session() as session:
        exists = (await session.execute(select(User.id).where(User.id == id_).limit(1))).one_or_none()
        if exists is None:
            user = User(id=id_)
            session.add(user)
            await session.commit()
    logger.success(f"[{id_}] Registered user")


async def check_user_exists(id_: int) -> bool:
    async with async_session() as session:
        exists = (await session.execute(select(User.id).where(User.id == id_).limit(1))).one_or_none()
    if exists is None:
        return False
    return True


async def get_users_by_status(status: str = 'alive') -> list[FunnelUser]:
    """Статус по умолчанию 'alive'"""
    # finish_day = max([int(day) for day in FunnelConfig.config.diff_days_to_func])
    finish_day = 20
    end = f'{finish_day + 1}-0'
    async with async_session() as session:
        stmt = select(User.id, User.funnel_timestamp,
                      User.funnel, User.step,
                      User.last_message_at_user, User.last_message_at_bot
                      )\
            .where(User.status == status, User.funnel.is_not(None), User.step != end)
        users = (await session.execute(stmt)).all()
    return users


async def get_users_without_funnel() -> list[int]:
    async with async_session() as session:
        stmt = select(User.id).where(User.funnel.is_(None), User.status == 'alive')
        users = (await session.execute(stmt)).scalars().all()
    return users


async def is_user_waiting_funnel(id_: int) -> bool:
    async with async_session() as session:
        stmt = select(User.id).where(User.id == id_, User.funnel.is_(None), User.status == 'alive')
        is_waiting = (await session.execute(stmt)).scalar_one_or_none() is not None
    return is_waiting


async def set_user_funnel(id_: int, funnel: str) -> None:
    async with async_session() as session:
        stmt = update(User).where(User.id == id_).values(funnel=funnel)
        await session.execute(stmt)
        await session.commit()


async def get_user_funnel(id_: int) -> str | None:
    async with async_session() as session:
        funnel = (await session.execute(select(User.funnel).where(User.id == id_))).scalar_one()
    return funnel


async def get_user_step(id_: int):
    async with async_session() as session:
        step = (await session.execute(select(User.step).where(User.id == id_))).scalar_one()
    return step


async def get_count_users_today():
    query = select(func.count(User.id)).where(func.DATE(User.registration_date) == date.today())
    async with async_session() as session:
        count = (await session.execute(query)).scalar_one()
    return count


async def set_status(id_: int, status: str):
    """Обновление статуса"""
    async with async_session() as session:
        await session.execute(update(User).values(status=status).where(User.id == id_))
        await session.commit()
        logger.info(f"DATABASE | [{id_}] Update User status - {status}")


async def set_day_message(id_: int, day: int, message: int):
    """Обновление полученного дня и сообщения"""
    async with async_session() as session:
        await session.execute(update(User).values(step=f'{day}-{message}').where(User.id == id_))
        await session.commit()
        logger.info(f"DATABASE | [{id_}] Update User step - {day}-{message}")


async def update_last_message_at_bot(id_: int):
    """Обновление последнего сообщения от нас"""
    async with async_session() as session:
        await session.execute(update(User).values(last_message_at_bot=func.now()).where(User.id == id_))
        await session.commit()
        logger.info(f"DATABASE | [{id_}] Update last message at bot")


async def update_last_message_at_user(id_: int):
    """Обновление последнего сообщения от юзера"""
    async with async_session() as session:
        await session.execute(update(User).values(last_message_at_user=func.now()).where(User.id == id_))
        await session.commit()
        logger.info(f"DATABASE | [{id_}] Update last message at user")


async def get_funnel_timestamp(id_: int):
    async with async_session() as session:
        funnel_tmp = (await session.execute(select(User.funnel_timestamp).where(User.id == id_))).scalar_one_or_none()
    return funnel_tmp


async def get_user_reply(id_: int):
    async with async_session() as session:
        user_reply = (await session.execute(select(User.last_message_at_user).where(User.id == id_))).scalar_one_or_none()
    return user_reply


async def get_bot_reply(id_: int):
    async with async_session() as session:
        bot_reply = (await session.execute(select(User.last_message_at_bot).where(User.id == id_))).scalar_one_or_none()
    return bot_reply


async def increase_being_late(id_: int, interval: timedelta):
    async with async_session() as session:
        await session.execute(update(User).values(being_late=User.being_late + interval).where(User.id == id_))
        await session.commit()
        logger.info(f"DATABASE | [{id_}] Increased being_late on ({interval})")

