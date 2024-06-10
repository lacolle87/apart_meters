from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

from database.database import Database
from utils.utils import format_metrics

router = Router()

db = Database()

@router.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Welcome! Send me your water metrics in the format: 'amount unit', e.g., '200 ml'.")


@router.message(Command('help'))
async def help_message(message: Message):
    await message.answer("You can send your water intake metrics in the format: 'amount unit', e.g., '200 ml'.\n"
                         "Commands:\n"
                         "/start - Start the bot\n"
                         "/help - Get help\n"
                         "/metrics - View your water metrics")


@router.message(Command('metrics'))
async def view_metrics(message: Message):
    user_id = message.from_user.id
    metrics = db.get_metrics(user_id)
    response = format_metrics(metrics)
    await message.answer(response)


@router.message()
async def record_metrics_handler(message: Message):
    user_id = message.from_user.id
    text = message.text
    amount, unit = text.split()

    recorded_amount, recorded_unit = db.add_metrics(user_id, amount, unit)
    if recorded_amount is not None:
        await message.answer(f"Recorded: {recorded_amount} {recorded_unit}")
    else:
        await message.answer("Failed to record metrics. Please try again.")
