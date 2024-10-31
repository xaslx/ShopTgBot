import asyncio
from aiogram import Bot, Dispatcher
from config import env_config
from aiogram.client.default import DefaultBotProperties
from logger import logger
from database import async_session_maker
from src.middleware import DbMiddleware
from src.users.handlers import user_handler
from src.admins.handlers import admin_handler


async def on_startup():
    logger.info('Бот включен')
    

async def on_shutdown():
    logger.info('Бот выключен')


async def main():
    bot: Bot = Bot(token=env_config.TOKEN_BOT, default=DefaultBotProperties(parse_mode='HTML'))
    dp: Dispatcher = Dispatcher()
    dp.update.middleware.register(DbMiddleware(async_session_maker))
    dp.include_router(admin_handler)
    dp.include_router(user_handler)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)




if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')



