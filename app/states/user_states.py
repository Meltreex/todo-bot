from aiogram.dispatcher.filters.state import State, StatesGroup

class CreateTask(StatesGroup):
    title = State()
    description = State()

class TaskID(StatesGroup):
    id = State()

class DelTaskId(StatesGroup):
    id = State()