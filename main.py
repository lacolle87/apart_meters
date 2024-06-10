import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.bot import router

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=API_TOKEN)

    dp = Dispatcher()

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received, stopping the program gracefully.")
    finally:
        db.close_database()


if __name__ == '__main__':
    asyncio.run(main())
