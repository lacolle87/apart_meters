import logging
import asyncio
from aiogram import Dispatcher, Router
from handlers.bot_handler import BotHandler
from loader.loader import init_bot, init_database
from database.services import MetricRepository
from logger.logger import setup_logger


async def main(bot_instance, dispatcher, logger_instance):
    try:
        await dispatcher.start_polling(bot_instance)
    except Exception as e:
        logger_instance.error(f"An error occurred: {e}")
    finally:
        logger_instance.info("Shutting down...")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = setup_logger()

    bot = init_bot(logger)
    db = init_database(logger)
    dp = Dispatcher()

    db_session = db.get_session()
    db_repository = MetricRepository(db_session, logger)

    router = Router()

    BotHandler(router, db_repository)

    dp.include_router(router)

    try:
        asyncio.run(main(bot, dp, logger))
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping the program gracefully.")
    finally:
        logger.info(db.close())
