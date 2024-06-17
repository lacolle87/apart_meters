import os
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from services.metric_service import MetricService
from services.apartment_service import ApartmentService
from services.user_service import UserService
from handlers.middleware import AuthMiddleware
from handlers.apartment_handler import ApartmentHandler, AddApartment
from handlers.metrics_handler import MetricsHandler, AddMetrics
from handlers.user_handler import UserHandler, AddUser
from handlers.command_handler import CommandHandlers


class BotSetup:
    def __init__(self, bot: Bot, router: Router, db_session, logger):
        self.bot = bot
        self.router = router
        self.logger = logger

        self.user_service = UserService(db_session, logger)
        self.apartment_service = ApartmentService(db_session, logger)
        self.metric_service = MetricService(db_session, logger)

        self.auth_middleware = AuthMiddleware(self.user_service, self.bot)

        self.add_apartment_handler = ApartmentHandler(self.apartment_service)
        self.add_metrics_handler = MetricsHandler(self.metric_service)
        self.add_user_handler = UserHandler(self.user_service, self.logger)
        self.command_handlers = CommandHandlers()
        self.view_metrics_handler = MetricsHandler(self.metric_service)

        self.setup_handlers()

    def setup_handlers(self):
        self.router.message.middleware(self.auth_middleware)

        self.router.message.register(
            self.command_handlers.send_welcome, Command('start'))
        self.router.message.register(
            self.command_handlers.help_message, Command('help'))
        self.router.message.register(
            self.view_metrics_handler.view_metrics, Command('metrics'))
        self.router.message.register(
            self.add_apartment_handler.add_apartment_start, Command('addapartment'))
        self.router.message.register(
            self.add_apartment_handler.apartment_name_entered, AddApartment.waiting_for_apartment_name)
        self.router.message.register(
            self.add_apartment_handler.apartment_address_entered, AddApartment.waiting_for_apartment_address)
        self.router.message.register(
            self.add_metrics_handler.add_metrics_start, Command('addmetrics'))
        self.router.message.register(
            self.add_metrics_handler.metrics_entered, AddMetrics.waiting_for_metrics)
        self.router.message.register(
            self.add_user_handler.add_user_start, Command('adduser'))
        self.router.message.register(
            self.add_user_handler.user_entered, AddUser.waiting_for_user_name)

        async def default_handler(message: Message):
            await self.auth_middleware.process_approval(message)
        self.router.message.register(default_handler)

    def init_su(self):
        try:
            su = int(os.getenv('SUPERUSER'))
            superuser = self.user_service.get_user_by_chat_id(su)
            if superuser and superuser.is_admin:
                self.logger.info(f"Superuser found")
            elif superuser and not superuser.is_admin:
                self.user_service.make_admin(su)
                self.logger.info(f"Superuser made admin")
            else:
                self.user_service.add_user(su, 'superuser', 'superuser', 0, False)
                self.user_service.make_admin(su)
                self.logger.info(f"Superuser not found, added and made admin")
        except Exception as e:
            self.logger.error(f"Failed to initialize superuser: {e}")
