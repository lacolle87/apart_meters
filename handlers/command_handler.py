from aiogram.types import Message


class CommandHandlers:
    @staticmethod
    async def send_welcome(message: Message):
        await message.answer("Welcome! Send me your water metrics in the format: 'amount unit', e.g., '200 ml'.")

    @staticmethod
    async def help_message(message: Message):
        await message.answer(
            "You can send your water intake metrics in the format: 'amount unit', e.g., '200 ml'.\n"
            "Commands:\n"
            "/start - Start the bot\n"
            "/help - Get help\n"
            "/metrics - View your water metrics\n"
            "/addmetrics - Add your water and electric metrics\n"
            "/addapartment - Add a new apartment")
