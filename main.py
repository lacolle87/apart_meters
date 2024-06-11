import logging
import asyncio
from aiogram import Dispatcher, Router
from handlers.bot import BotHandler
from loader.loader import init_bot, init_database
from database.repositories import WaterMetricRepository


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = init_bot()
    db = init_database()
    dp = Dispatcher()

    db_session = db.get_session()
    db_repository = WaterMetricRepository(db_session)

    router = Router()

    BotHandler(router, db_repository)

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received, stopping the program gracefully.")
    finally:
        logging.info(db.close())


if __name__ == '__main__':
    asyncio.run(main())
