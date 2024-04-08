from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .models import Base

from .models.users import Users
from sqlalchemy import Select

async def sql_connect(url:str): # Функция для подключения к БД
    sql = create_async_engine(url)
    async def init_models():
        async with sql.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    await init_models()
    return AsyncSession(sql)


async def get_lang(db:AsyncSession,user_id): # Функция для получения языка к БД
    async with db as session:
        result = await session.execute(Select(Users.lang).where(Users.tg_id == user_id))
        result = result.fetchone()[0]
        await session.flush()
        await session.commit()
    return result