from aiogram.filters import Filter
from aiogram.types import Message
import os
from config import env_config

ADMINS: list[int] = env_config.ADMINS_ID


class AdminProtect(Filter):

    def __init__(self):
        self.admins: list[int] = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins