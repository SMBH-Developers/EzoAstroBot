from src.constants import FILES_DIR

from ...dispatcher.filters import RegistrationTimeFilter, BotReplyFilter, UserReplyFilter
from ...dispatcher.types import MyGeneratedMessage
from ..base import BaseFunnelDays, BaseFunnelConfig
from ._texts import *


DefaultF = RegistrationTimeFilter


class _FunnelDays(BaseFunnelDays):

    def __init__(self):
        self.days = {
            "0": self.first_day, "1": self.second_day, "2": self.third_day,
            "3": self.fourth_day, "4": self.fifth_day, "5": self.sixth_day,
            "6": self.seventh_day, "7": self.eighth_day, "8": self.ninth_day
        }

    @staticmethod
    def first_day():
        """Первый день"""
        day_message = [
            MyGeneratedMessage(DefaultF.create(6), 0, 'text', {'text': FirstDayTexts.msg_1}, last_message=True),
        ]
        return day_message

    @staticmethod
    def second_day():
        """Второй день"""
        day_message = [
            MyGeneratedMessage(DefaultF.create(17), 0, 'text', {'text': SecondDayTexts.msg_1}, last_message=True)

        ]
        return day_message

    @staticmethod
    def third_day():
        """Третий день"""
        directory = FILES_DIR / 'day_3'
        day_message = [
            MyGeneratedMessage(DefaultF.create(21), 0, 'text', {'text': ThirdDayTexts.msg_1}),
            MyGeneratedMessage(DefaultF.create(13), 7, 'document', {'document': directory / 'Финансовый_код.pdf'}, last_message=True),
        ]
        return day_message
    
    @staticmethod
    def fourth_day():
        """Четвертый день"""
        day_message = [
            MyGeneratedMessage(DefaultF.create(15), 0, 'text', {'text': FourthDayTexts.msg_1}, last_message=True)
        ]
        return day_message

    @staticmethod
    def sixth_day():
        """Шестой день"""
        day_message = [
            MyGeneratedMessage(DefaultF.create(10), 0, 'text', {'text': SixthDayTexts.msg_1}, last_message=True)
        ]
        return day_message

    @staticmethod
    def seventh_day():
        """Седьмой день"""
        day_message = [
            MyGeneratedMessage(DefaultF.create(18), 0, 'text', {'text': SeventhDayTexts.msg_1}, last_message=True)
        ]
        return day_message

    @staticmethod
    def eighth_day():
        """Восьмой день"""
        day_message = [
            MyGeneratedMessage(DefaultF.create(12), 0, 'text', {'text': EighthDayTexts.msg_1}, last_message=True)
        ]
        return day_message

    @staticmethod
    def ninth_day():
        """Девятый день"""
        day_message = [
            MyGeneratedMessage(DefaultF.create(5), 0, 'text', {'text': NinthDayTexts.msg_1}, last_message=True)
        ]
        return day_message


class FunnelConfig(BaseFunnelConfig):

    title = 'funnel'
    config = _FunnelDays()
    skip_days = []
