import logging
import asyncio
from aiogram import Dispatcher, Router
from loader.loader import init_bot, init_database
from logger.logger import setup_logger
from setup.bot_setup import BotSetup


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

    router = Router()

    bot_setup = BotSetup(bot, router, db_session, logger)

    bot_setup.init_su()

    dp.include_router(router)

    try:
        asyncio.run(main(bot, dp, logger))
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping the program gracefully.")
    finally:
        logger.info(db.close())
