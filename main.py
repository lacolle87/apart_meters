import logging
import asyncio
from aiogram import Dispatcher
from handlers.bot import router
from loader.loader import init_bot, init_database


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = init_bot()
    db = init_database()
    dp = Dispatcher()

    dp.include_router(router)

    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received, stopping the program gracefully.")
    finally:
        print(db.close_database)

if __name__ == '__main__':
    asyncio.run(main())
