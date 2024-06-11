import logging
import asyncio
from aiogram import Dispatcher, Router
from handlers.bot_handler import BotHandler
from loader.loader import init_bot, init_database
from database.repositories import WaterMetricRepository
from logger.logger import setup_logger


async def main():
    logging.basicConfig(level=logging.INFO)
    logger = setup_logger()

    bot = init_bot(logger)
    db = init_database(logger)
    dp = Dispatcher()

    db_session = db.get_session()
    db_repository = WaterMetricRepository(db_session)

    router = Router()

    BotHandler(router, db_repository)

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logger.info("Program was cancelled.")
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping the program gracefully.")
    finally:
        logger.info(db.close())


if __name__ == '__main__':
    asyncio.run(main())
