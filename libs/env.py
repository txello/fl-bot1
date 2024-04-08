from envserv import EnvBase, variable

class BotEnv(EnvBase): # Переменные окружения для бота
    __envfile__ = '.env'
    token:str = variable(alias='TG_TOKEN', overwrite=False)

class NotionEnv(EnvBase): # Переменные окружения для Notion
    __envfile__ = '.env'
    token:str = variable(alias='NOTION_TOKEN', overwrite=False)
    
class DatabaseEnv(EnvBase): # Переменные окружения для PostgreSQL
    __envfile__ = '.env'
    login:str = variable(alias='SQL_LOGIN', overwrite=False)
    password:str = variable(alias='SQL_PASSWORD', overwrite=False)
    host:str = variable(alias='SQL_HOST', overwrite=False)
    port:str = variable(alias='SQL_PORT', overwrite=False)
    name:str = variable(alias='SQL_NAME', overwrite=False)
    
bot_env = BotEnv()
notion_env = NotionEnv()
db_env = DatabaseEnv()