from typing import Callable, Dict, Any, Awaitable
 
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker





class DbMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker):
        self.factory = session_factory
 
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.factory() as session:
            data['session'] = session
            return await handler(event, data)