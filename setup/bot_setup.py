import os
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from services.metric_service import MetricService
from services.apartment_service import ApartmentService
from services.user_service import UserService
from middleware.auth_middleware import AuthMiddleware
from handlers.apartment_handler import ApartmentHandler, AddApartment
from handlers.metrics_handler import MetricsHandler, AddMetrics
from handlers.user_handler import UserHandler, AddUser
from handlers.command_handler import CommandHandlers
from filters.is_admin_filter import IsAdmin


class BotSetup:
    def __init__(self, bot: Bot, router: Router, db_session, logger):
        self.bot = bot
        self.router = router
        self.logger = logger

        self.user_service = UserService(db_session, logger)
        self.apartment_service = ApartmentService(db_session, logger)
        self.metric_service = MetricService(db_session, logger)

        self.auth_middleware = AuthMiddleware(self.user_service, self.bot)

        self.is_admin_filter = IsAdmin(self.user_service)

        self.add_apartment_handler = ApartmentHandler(self.apartment_service)
        self.add_metrics_handler = MetricsHandler(self.metric_service)
        self.add_user_handler = UserHandler(self.user_service, self.logger)
        self.command_handlers = CommandHandlers()
        self.view_metrics_handler = MetricsHandler(self.metric_service)

        # Setup message handlers
        self.setup_message_handlers()

    def setup_message_handlers(self):
        self.router.message.middleware(self.auth_middleware)

        self.register_command_handlers()

        self.register_admin_handlers()

        self.register_authorization_handlers()

    def register_command_handlers(self):
        commands = [
            ('start', self.command_handlers.send_welcome),
            ('help', self.command_handlers.help_message),
            ('metrics', self.view_metrics_handler.view_metrics)
        ]
        for command, handler in commands:
            self.router.message.register(handler, Command(command))

    def register_admin_handlers(self):
        admin_handlers = [
            ('addapartment', self.add_apartment_handler.add_apartment_start, self.is_admin_filter),
            ('addmetrics', self.add_metrics_handler.add_metrics_start, self.is_admin_filter),
            ('adduser', self.add_user_handler.add_user_start, self.is_admin_filter)
        ]
        for command, handler, filter_ in admin_handlers:
            self.router.message.register(handler, Command(command), filter_)

        apartment_subhandlers = [
            (AddApartment.waiting_for_apartment_name, self.add_apartment_handler.apartment_name_entered),
            (AddApartment.waiting_for_apartment_address, self.add_apartment_handler.apartment_address_entered)
        ]
        for state, handler in apartment_subhandlers:
            self.router.message.register(handler, state)

        metrics_subhandlers = [
            (AddMetrics.waiting_for_metrics, self.add_metrics_handler.metrics_entered)
        ]
        for state, handler in metrics_subhandlers:
            self.router.message.register(handler, state)

        user_subhandlers = [
            (AddUser.waiting_for_user_name, self.add_user_handler.user_entered)
        ]
        for state, handler in user_subhandlers:
            self.router.message.register(handler, state)

    def register_authorization_handlers(self):
        self.router.message.register(self.auth_middleware.process_approval, self.is_admin_filter)
        self.router.message.register(self.reject_unauthorized)

    @staticmethod
    async def reject_unauthorized(message: Message):
        await message.answer("You are not authorized to use this command.")

    def init_su(self):
        try:
            su = int(os.getenv('SUPERUSER'))
            superuser = self.user_service.get_user_by_chat_id(su)
            if superuser:
                if not superuser.is_admin:
                    self.user_service.make_admin(su)
                    self.logger.info(f"Superuser made admin")
            else:
                self.user_service.add_user(su, 'superuser', 'superuser', 0, False)
                self.user_service.make_admin(su)
                self.logger.info(f"Superuser not found, added and made admin")
        except Exception as e:
            self.logger.error(f"Failed to initialize superuser: {e}")
