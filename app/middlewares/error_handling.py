from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
import logging

logger = logging.getLogger("aiogram")

class ErrorHandlingMiddleware(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):
        try:
            pass
        except Exception as exception:
            logger.error(f"{exception.__class__.__name__}: {str(exception)}")
            await msg.answer("Произошла ошибка. Пожалуйста, попробуйте снова.")
            raise exception