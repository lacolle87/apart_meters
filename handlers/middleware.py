from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from services.user import UserService


class AuthMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        user = self.user_service.get_user_by_chat_id(user_id)
        if not user:
            await event.answer("You need to be authenticated to use this bot. Please register first.")
            return
        return await handler(event, data)
