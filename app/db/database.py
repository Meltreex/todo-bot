import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg)

async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass