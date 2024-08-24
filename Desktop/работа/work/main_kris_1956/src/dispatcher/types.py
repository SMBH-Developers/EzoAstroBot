from enum import Enum
from pathlib import Path
from dataclasses import dataclass
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from .filters.base import BaseFilter


class Timepoint(Enum):
    registration_date = "registration_date"
    user_reply = "user_reply"
    bot_reply = "bot_reply"


@dataclass
class MyGeneratedMessage:
    filter: "BaseFilter"
    seconds_wait_before_sending: int
    content_type_to_send: str
    others_kwargs: dict
    trigger_from_our_account_to_cancel: list | None = None
    last_message: bool = False

    def __post_init__(self):
        self.filter.message = self

        if self.content_type_to_send in ('document', 'audio'):  # Changing to normal filename
            self.others_kwargs['file_name'] = self.others_kwargs[self.content_type_to_send].name

        file = self.others_kwargs.get(self.content_type_to_send)
        if isinstance(file, Path) and not file.exists():  # Check that file exists
            logger.warning(f'{file} is not found. Stop funnel')
