from datetime import datetime, timedelta

from sqlalchemy import BIGINT, TIMESTAMP, Interval, String, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from src.enum import Status


__all__ = ["Base", "User"]


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    registration_date: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    step: Mapped[str] = mapped_column(String(64), server_default='0-0', comment='Format: {day}-{message} or {day}-*')
    funnel: Mapped[str | None] = mapped_column(String(64))

    status: Mapped[str] = mapped_column(String(64), server_default=Status.ALIVE.value)

    last_message_at_user: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    last_message_at_bot: Mapped[datetime | None] = mapped_column(TIMESTAMP)

    being_late: Mapped[timedelta] = mapped_column(Interval, server_default=text("INTERVAL '0 second'"))

    @hybrid_property
    def funnel_timestamp(self) -> datetime:
        return self.registration_date + self.being_late


class UserTag(Base):
    __tablename__ = 'users_tags'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    name: Mapped[str] = mapped_column(String(64), comment="tag's name")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
