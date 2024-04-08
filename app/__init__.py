from libs.env import db_env
from plugins.postgresql import sql_connect

async def conn(): # Функция подключения
    return await sql_connect(f"postgresql+asyncpg://{db_env.login}:{db_env.password}@{db_env.host}:{db_env.port}/{db_env.name}")
