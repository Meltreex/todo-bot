from aiogram import types, executor
from aiogram.dispatcher.filters import CommandHelp, ChatTypeFilter

from main import dp
from app.db.OrmQuery import AsyncOrmQuery
from app.db.dbstruct import UserOrm
from app.models.user import UserCreate


@dp.message_handler(CommandHelp(), ChatTypeFilter(types.ChatType.PRIVATE), state='*')
async def cmd_start(msg: types.Message):
    msg.answer('help')