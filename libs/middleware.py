from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from settings import apps


class TestMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Any:
        user = data["event_from_user"] # Получаем пользователя
        if user.id in apps.users: # Если ID пользователя есть в apps.users, то функции работают
            return await handler(event,data)