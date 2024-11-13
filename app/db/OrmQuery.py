from sqlalchemy import select, and_

from app.db.database import async_engine, async_session_factory, Base
from app.db.dbstruct import UserOrm, TaskOrm
from app.models.task import TaskCreate

class AsyncOrmQuery: 
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    @staticmethod
    async def insert_data(first_name: str, username: str):
        async with async_session_factory() as session:
            new_user = UserOrm(
                first_name=first_name,
                username=username
            )
            session.add(new_user)
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_username_user(username: str):
        async with async_session_factory() as session:
            query = select(UserOrm).filter(UserOrm.username==username)
            res = await session.execute(query)
            result = res.scalars().first()
            return result
        
    @staticmethod
    async def insert_task(task: TaskCreate, owner_id: int): 
        async with async_session_factory() as session:
            task_query = TaskOrm(**task.dict(), owner_id=owner_id)
            session.add(task_query)
            await session.flush()
            await session.commit()
            await session.refresh(task_query)

    @staticmethod
    async def select_tasks(owner_id: int, skip: int, limit: int):
        async with async_session_factory() as session:
            query = select(TaskOrm).filter(
                TaskOrm.owner_id == owner_id
            ).offset(skip).limit(limit)
            res = await session.execute(query)
            result = res.scalars().all()
            return result
        
    @staticmethod
    async def select_task_for_id(task_id: int, owner_id: int):
        async with async_session_factory() as session:
            query = select(TaskOrm).filter(
                and_(
                    TaskOrm.id == task_id,
                    TaskOrm.owner_id == owner_id
                )
                )
            res = await session.execute(query)
            result = res.scalars().first()
            return result
        
    @staticmethod
    async def delete_task(task_id: int, owner_id: int):
        async with async_session_factory() as session:
            query = select(TaskOrm).filter(
                and_(
                    TaskOrm.id == task_id, 
                    TaskOrm.owner_id == owner_id
                )
            ) 
            res = await session.execute(query)
            result = res.scalars().first()
            if result is None:
                return None
            
            await session.delete(result)
            await session.commit()