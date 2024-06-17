from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from services.user_service import UserService
from aiogram import Bot
from handlers.user_approval_handler import UserApprovalHandler
from utils.admin_notifier import AdminNotifier


class AuthMiddleware(BaseMiddleware):
    def __init__(self, user_service: UserService, bot: Bot):
        super().__init__()
        self.user_service = user_service
        self.bot = bot
        self.pending_approvals = {}
        self.approval_handler = UserApprovalHandler(user_service, bot, self.pending_approvals)
        self.notifier = AdminNotifier(user_service, bot)

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        user = self.user_service.get_user_by_chat_id(user_id)

        if user:
            return await handler(event, data)

        await self.handle_unregistered_user(event, user_id)

    async def handle_unregistered_user(self, event: Message, user_id: int):
        if user_id in self.pending_approvals:
            await event.answer("Your registration is pending approval. Please wait for the superuser to confirm.")
            return

        await event.answer("You are not registered. Waiting for approval.")
        await self.notifier.notify_admin_of_new_user(event, user_id)
        self.pending_approvals[user_id] = event.from_user.username
