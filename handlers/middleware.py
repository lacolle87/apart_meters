from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from services.user import UserService
from aiogram import Bot


class AuthMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService, bot: Bot):
        super().__init__()
        self.user_service = user_service
        self.bot = bot
        self.pending_approvals = {}

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        user = self.user_service.get_user_by_chat_id(user_id)
        admins = self.user_service.get_admins()

        if not user:
            if user_id in self.pending_approvals:
                await event.answer("Your registration is pending approval. Please wait for the superuser to confirm.")
                return

            await self.bot.send_message(
                admins[0].chat_id,
                f"New user {event.from_user.username} ({user_id}) is trying to access the bot. Approve? Reply with 'yes' or 'no'."
            )
            self.pending_approvals[user_id] = event.from_user.username
            return

        return await handler(event, data)

    async def process_approval(self, message: Message):
        admin_id = message.from_user.id
        admins = self.user_service.get_admins()
        if admin_id != admins[0].chat_id:
            await message.answer("You are not authorized to approve users.")
            return

        response = message.text.lower().strip()
        if response == 'yes':
            await self.handle_approval(message, True)
        elif response == 'no':
            await self.handle_approval(message, False)
        else:
            await message.answer("Please reply with 'yes' or 'no'.")

    async def handle_approval(self, message: Message, approved: bool):
        if not self.pending_approvals:
            await message.answer("There are no pending user approvals.")
            return

        user_id, username = next(iter(self.pending_approvals.items()))
        if approved:
            await self.approve_user(user_id, username)
        else:
            await self.deny_user(user_id)

    async def approve_user(self, user_id: int, username: str):
        self.user_service.add_user(user_id, username, username, 0, False)
        await self.bot.send_message(user_id, "Your registration has been approved. You can now use the bot.")
        del self.pending_approvals[user_id]

    async def deny_user(self, user_id: int):
        if user_id in self.pending_approvals:
            del self.pending_approvals[user_id]
            await self.bot.send_message(user_id, "Your registration has been denied.")
