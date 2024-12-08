from aiogram.filters import Filter
from aiogram import Bot, types

import api
from database.orm_query import orm_get_user
from sqlalchemy.ext.asyncio import AsyncSession


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]):
        self.chat_types = chat_types

    async def __call__(self, message: types.Message):
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message, session: AsyncSession):
        if not orm_get_user(session, message.from_user.id):
            return False
        return True
