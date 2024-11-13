from aiogram import types, Dispatcher, Bot, executor
import logging
from app.middlewares.logging import LoggingMiddleware
from app.middlewares.error_handling import ErrorHandlingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config import settings
from app.db.database import Base, async_engine
from app.db.OrmQuery import AsyncOrmQuery

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)
logging.info("Бот запущен!")

dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(ErrorHandlingMiddleware())

async def on_start(dp):
    await AsyncOrmQuery.create_tables()

if __name__ == '__main__':
    from app.handlers import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)