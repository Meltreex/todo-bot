from aiogram import types, executor
from aiogram.dispatcher.filters import Command, ChatTypeFilter
from aiogram.dispatcher import FSMContext

from main import dp
from app.db.OrmQuery import AsyncOrmQuery
from app.db.dbstruct import UserOrm
from app.models.task import TaskResponseId
from app.states.user_states import DelTaskId



@dp.message_handler(Command("del_task_id"), ChatTypeFilter(types.ChatType.PRIVATE), state='*')
async def cmd_start(msg: types.Message):
    await msg.answer("Введите Id задачи которую хотите удалить: ")
    await DelTaskId.id.set()

@dp.message_handler(state=DelTaskId.id)
async def cmd_start(msg: types.Message, state: FSMContext):
    try: 
        await state.update_data(id=msg.text)

        user_data = await state.get_data()
        
        user = await AsyncOrmQuery.select_username_user(username=msg.from_user.username)

        id = TaskResponseId(id=int(user_data["id"]))

        response = await AsyncOrmQuery.select_task_for_id(id.id, user.id)
        if response is None:
            await msg.answer(f"Записи с таким номером не найдено!")
            await state.finish()
        
        await AsyncOrmQuery.delete_task(id.id, user.id)
        await msg.answer(f"Задача удалена!")
        
    except Exception as e:
        await state.finish()
        print(e)