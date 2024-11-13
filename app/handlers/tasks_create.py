from aiogram import types, executor
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter, Command
from aiogram.dispatcher import FSMContext

from main import dp
from app.db.OrmQuery import AsyncOrmQuery
from app.db.dbstruct import UserOrm
from app.models.task import TaskCreate
from app.middlewares.error_handling import logger
from app.states.user_states import CreateTask


@dp.message_handler(Command("new_task"), state="*")
async def create_task_notify(msg: types.Message):
    try:
        await msg.answer("Введите новую запись.\nНачните с заголовка!")
        await CreateTask.title.set()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

@dp.message_handler(state=CreateTask.title)
async def create_task_title(msg: types.Message, state: FSMContext):
    try:
        await state.update_data(title=msg.text.lower())
        await msg.answer("А сейчас введите описание: ")
        await CreateTask.next()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        state.finish()

@dp.message_handler(state=CreateTask.description)
async def create_task_title(msg: types.Message, state: FSMContext):
    try:
        await state.update_data(description=msg.text.lower())

        user_data = await state.get_data()

        user = await AsyncOrmQuery.select_username_user(username=msg.from_user.username)

        task = TaskCreate(title=user_data["title"], description=user_data["description"])

        task_db = await AsyncOrmQuery.insert_task(task=task, owner_id=user.id)
        await msg.answer("Запись добавлена!")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        state.finish()