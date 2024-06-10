from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router

water_metrics = {}

router = Router()

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
    if user_id in water_metrics:
        metrics = water_metrics[user_id]
        response = "Your water metrics:\n" + "\n".join([f"{amount} {unit}" for amount, unit in metrics])
    else:
        response = "You have not recorded any water metrics yet."
    await message.answer(response)

@router.message()
async def record_metrics(message: Message):
    user_id = message.from_user.id
    text = message.text

    try:
        amount, unit = text.split()
        amount = float(amount)
    except ValueError:
        await message.answer("Invalid format. Please send in the format: 'amount unit', e.g., '200 ml'.")
        return

    if user_id not in water_metrics:
        water_metrics[user_id] = []

    water_metrics[user_id].append((amount, unit))
    await message.answer(f"Recorded: {amount} {unit}")