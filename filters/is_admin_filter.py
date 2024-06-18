from aiogram import types
from aiogram.filters import Filter
from services.user_service import UserService


class IsAdmin(Filter):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def __call__(self, message: types.Message):
        user = self.user_service.get_user_by_chat_id(message.from_user.id)
        return user.is_admin
