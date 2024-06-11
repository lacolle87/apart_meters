from dotenv import load_dotenv
import os
from aiogram import Bot
from database.database import Database


def init_bot():
    load_dotenv()

    api_token = os.getenv('API_TOKEN')
    bot = Bot(token=api_token)
    return bot


def init_database():
    engine = 'sqlite:///water_metrics.db'
    db = Database(engine)
    return db
