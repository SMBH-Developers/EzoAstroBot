from sqlalchemy.orm import declarative_base, mapped_column, Mapped

from sqlalchemy import (
    BIGINT,
    String,
    TIMESTAMP,
    func,
    text
)

from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    advice_step: Mapped[int] = mapped_column(server_default=text('0'))
    birth_date: Mapped[str | None] = mapped_column(String(128))
    horoscope_text_index: Mapped[int | None] = mapped_column()  # Индекс текста который им выпал
    apply_code: Mapped[str | None] = mapped_column(String(16))

    got_2h_autosending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    got_24h_autosending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    got_48h_autosending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    got_72h_autosending: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    black_friday_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    bf_state: Mapped[str | None] = mapped_column(String(64))

    black_friday_sending_2: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    bf_state_2: Mapped[str | None] = mapped_column(String(64))

    black_friday_sending_3: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    bf_state_3: Mapped[str | None] = mapped_column(String(64))

    nov15_sending_1: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    nov20_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    nov21_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    nov22_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    nov22_2_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    bf_22nov: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    bf_2_22nov: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    nov24_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    nov24_marathon_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    nov25_marathon_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    dec5_sending_1: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    dec5_sending_2: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    dec10_sending: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    sending_29_feb: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    sending_10_march: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    sending_25_march: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    sending_4_april: Mapped[datetime | None] = mapped_column(TIMESTAMP)
    sending_24_april: Mapped[datetime | None] = mapped_column(TIMESTAMP)
