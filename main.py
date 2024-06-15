import logging
import asyncio
from aiogram import Dispatcher, Router
from handlers.bot_handler import BotHandler
from loader.loader import init_bot, init_database, init_su
from services.metric import MetricService
from services.apartment import ApartmentService
from services.user import UserService
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

    user_service = UserService(db_session, logger)
    apartment_service = ApartmentService(db_session, logger)
    metric_service = MetricService(db_session, logger)

    init_su(user_service, logger)

    router = Router()

    BotHandler(router, user_service, apartment_service, metric_service, logger)

    dp.include_router(router)

    try:
        asyncio.run(main(bot, dp, logger))
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping the program gracefully.")
    finally:
        logger.info(db.close())
