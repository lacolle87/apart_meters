from dotenv import load_dotenv
import os
from aiogram import Bot
from database.dbmanager import Database


def init_bot(logger):
    try:
        load_dotenv()
        api_token = os.getenv('API_TOKEN')
        bot = Bot(token=api_token)
        return bot
    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}")
        return None


def init_database(logger):
    try:
        engine = 'sqlite:///metrics.db'
        db = Database(engine, logger)
        return db
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return None


def init_su(user_service, logger):
    su = os.getenv('SUPERUSER')
    superuser = user_service.get_user_by_chat_id(su)
    if superuser and superuser.is_admin:
        logger.info(f"Superuser found")
    elif superuser and not superuser.is_admin:
        user_service.make_admin(su)
        logger.info(f"Superuser made admin")
    else:
        user_service.add_user(su, 'superuser', 'superuser', None, False)
        user_service.make_admin(su)
        logger.info(f"Superuser not found, added and made admin")
