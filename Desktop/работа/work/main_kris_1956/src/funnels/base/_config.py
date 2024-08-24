import inspect
from abc import ABC


class BaseFunnelDays:

    days: dict


class BaseFunnelConfig(ABC):

    title: str = NotImplemented
    config: BaseFunnelDays = NotImplemented
    skip_days: list[int] = NotImplemented

    @classmethod
    async def get_message(cls, user_id: int, day: int | str):
        func = cls.config.days[str(day)]

        args: list = []
        if 'id_' in func.__code__.co_varnames:
            args.append(user_id)

        if inspect.iscoroutine(func):
            # noinspection PyArgumentList,PyUnresolvedReferences
            return await func(*args)
        # noinspection PyArgumentList
        return func(*args)
