from dataclasses import dataclass, field
from string import Template

from aiogram import types, Bot
from aiogram.utils import markdown as m


@dataclass
class SendingData:
    uid: str
    text: str | Template
    url: str
    btn_title: str
    photo: str | None = None
    video: str | None = None

    kb: types.InlineKeyboardMarkup = field(init=False)
    count: int = field(init=False)

    async def get_text(self, bot: Bot, user_id: int, name: str = None):
        if isinstance(self.text, str):
            return self.text
        else:
            if name is None:
                chat_member = await bot.get_chat_member(user_id, user_id)
                name = chat_member.user.first_name
            name = m.quote_html(name)
            return self.text.substitute(name=name)

    def __post_init__(self):
        self.kb = types.InlineKeyboardMarkup()
        self.kb.add(types.InlineKeyboardButton(self.btn_title, url=self.url))
        self.count = 0


bf_sending = SendingData("sending_24_april",
                         Template(f'💵ТВОЙ КОШЕЛЕК ПОПОЛНИТСЯ ПОСЛЕ ЭТОГО 👇\n\n🎁Энергии зеркальной даты 24.04.2024 влияют на будущий финансовый поток \n\n💰Именно сегодня можно улучшить свое финансовое положение, приумножить достаток, начать получать дорогостоящие подарки, повышения на работе, предложения о партнерстве\n\n🔜Если хотите узнать как повысить свой доход с помощью денежных практик 24.04.2024, то скорее пишите в личные сообщение «ДЕНЬГИ» своему гуру @your_mentoor\n\n🌹Всего 7 мест для личной работы с гуру по улучшению твоих финансов, успевайте узнать подробности…'),
                         url="https://t.me/your_mentoor",
                         btn_title="Изменить жизнь"
                         )
