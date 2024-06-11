from dotenv import load_dotenv
import os
from aiogram import Bot
from database.database import Database


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
        engine = 'sqlite:///water_metrics.db'
        db = Database(engine)
        return db
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        return None
