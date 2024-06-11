from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
from utils.utils import format_metrics
from database.repositories import MetricRepository


class BotHandler:
    def __init__(self, router: Router, db_repository: MetricRepository):
        self.router = router
        self.db_repository = db_repository
        self.setup_handlers()

    def setup_handlers(self):
        @self.router.message(Command('start'))
        async def send_welcome(message: Message):
            await message.answer("Welcome! Send me your water metrics in the format: 'amount unit', e.g., '200 ml'.")

        @self.router.message(Command('help'))
        async def help_message(message: Message):
            await message.answer(
                "You can send your water intake metrics in the format: 'amount unit', e.g., '200 ml'.\n"
                "Commands:\n"
                "/start - Start the bot\n"
                "/help - Get help\n"
                "/metrics - View your water metrics")

        @self.router.message(Command('metrics'))
        async def view_metrics(message: Message):
            user_id = message.from_user.id
            metrics = self.db_repository.get_metrics_for_user(user_id)
            response = format_metrics(metrics)
            await message.answer(response)

        @self.router.message()
        async def record_metrics_handler(message: Message):
            user_id = message.from_user.id
            text = message.text
            try:
                amount, unit = text.split()
                amount = float(amount)

                recorded_amount, recorded_unit = self.db_repository.add_metrics_for_user(user_id, amount, unit)
                if recorded_amount is not None:
                    await message.answer(f"Recorded: {recorded_amount} {recorded_unit}")
                else:
                    await message.answer("Failed to record metrics. Please try again.")
            except ValueError:
                await message.answer("Invalid format. Please send in the format: 'amount unit', e.g., '200 ml'.")
