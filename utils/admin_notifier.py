from aiogram.types import Message
from services.user_service import UserService
from aiogram import Bot


class AdminNotifier:
    def __init__(self, user_service: UserService, bot: Bot):
        self.user_service = user_service
        self.bot = bot

    async def notify_admin_of_new_user(self, event: Message, user_id: int):
        admins = self.user_service.get_admins()
        await self.bot.send_message(
            admins[0].chat_id,
            f"New user {event.from_user.username} ({user_id}) is trying to access the bot. Approve? Reply with 'yes' or 'no'."
        )