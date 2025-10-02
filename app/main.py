import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import config
from app.database.models.base import Base
from app.handlers import start
from app.database.session import engine
from app.middleware.database_middleware import DataBaseSessionMiddleware


async def main():
    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Настройка бота
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.update.middleware(DataBaseSessionMiddleware())

    # Регистрация роутеров
    dp.include_router(start.router)
    # dp.include_router(catalog.router)
    # dp.include_router(cart.router)
    # dp.include_router(admin.router)

    # Запуск бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())