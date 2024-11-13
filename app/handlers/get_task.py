from aiogram import types, executor
from aiogram.dispatcher.filters import Command, ChatTypeFilter
from aiogram.dispatcher import FSMContext

from main import dp
from app.db.OrmQuery import AsyncOrmQuery
from app.db.dbstruct import UserOrm
from app.models.task import TaskResponseId
from app.states.user_states import TaskID


@dp.message_handler(Command("tasks"), ChatTypeFilter(types.ChatType.PRIVATE), state='*')
async def cmd_start(msg: types.Message, skip: int = 0, limit: int = 10):

    user = await AsyncOrmQuery.select_username_user(username=msg.from_user.username)

    tasks = await AsyncOrmQuery.select_tasks(owner_id=user.id, skip=skip, limit=limit)
    for task in tasks:
        await msg.answer(f"Ваши задачи №{task.id}: \n{task.title}\n{task.description}")


@dp.message_handler(Command("tasks_id"), ChatTypeFilter(types.ChatType.PRIVATE), state='*')
async def cmd_start(msg: types.Message):
    await msg.answer("Введите Id задачи которую хотите увидеть: ")
    await TaskID.id.set()

@dp.message_handler(state=TaskID.id)
async def cmd_start(msg: types.Message, state: FSMContext):
    try: 
        await state.update_data(id=msg.text)

        user_data = await state.get_data()
        
        user = await AsyncOrmQuery.select_username_user(username=msg.from_user.username)

        id = TaskResponseId(id=int(user_data["id"]))

        task_id = await AsyncOrmQuery.select_task_for_id(id.id, user.id)
        if task_id:
            await msg.answer(f"Ваши задачa №{task_id.id}: \n{task_id.title}\n{task_id.description}")
        else:
            await msg.answer("Записи с таким номером не найдено!")
            await state.finish()
    except Exception as e:
        await state.finish()
        print(e)