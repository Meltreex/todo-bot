import logging
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

logging.basicConfig(level=logging.INFO)

class LoggingMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        logging.info(f"Received message: {message.text} from {message.from_user.id}")
        logging.info(f"User info: {message.from_user.username}, {message.from_user.first_name}, {message.from_user.id}")
