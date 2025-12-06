from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import config

async_engine = create_async_engine(
    url = config.DATABASE_URL_ASYNCPG,
    echo = False
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session