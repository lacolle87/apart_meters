from aiogram.types import Message
from services.user_service import UserService
from aiogram import Bot


class UserApprovalHandler:
    def __init__(self, user_service: UserService, bot: Bot, pending_approvals: dict):
        self.user_service = user_service
        self.bot = bot
        self.pending_approvals = pending_approvals

    async def process_approval(self, message: Message):
        if not self.is_authorized_admin(message.from_user.id):
            await message.answer("You are not authorized to approve users.")
            return

        response = message.text.lower().strip()
        if response in ['yes', 'no']:
            await self.handle_approval(message, response == 'yes')
        else:
            await message.answer("Please reply with 'yes' or 'no'.")

    def is_authorized_admin(self, admin_id: int) -> bool:
        admins = self.user_service.get_admins()
        return admin_id == admins[0].chat_id

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
        self.remove_pending_approval(user_id)

    async def deny_user(self, user_id: int):
        if user_id in self.pending_approvals:
            self.remove_pending_approval(user_id)
            await self.bot.send_message(user_id, "Your registration has been denied.")

    def remove_pending_approval(self, user_id: int):
        if user_id in self.pending_approvals:
            del self.pending_approvals[user_id]
