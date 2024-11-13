from aiogram import types, executor
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter

from main import dp
from app.db.OrmQuery import AsyncOrmQuery
from app.db.dbstruct import UserOrm
from app.models.user import UserCreate


@dp.message_handler(CommandStart(), ChatTypeFilter(types.ChatType.PRIVATE), state='*')
async def cmd_start(msg: types.Message):

    user = UserCreate(first_name=msg.from_user.first_name, username=msg.from_user.username)

    if await AsyncOrmQuery.select_username_user(username=user.username) is None:

        await AsyncOrmQuery.insert_data(
            first_name=user.first_name,
            username=user.username
        )
        await msg.answer('Привет, бот запущен...\nПользователь зарегестрирован!')
    else:
        await msg.answer("Такой пользователь уже зарегестрирован!")