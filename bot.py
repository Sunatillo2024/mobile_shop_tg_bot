import asyncio
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.config import dp, TOKEN
from app.handlers.order import order_router
from app.handlers.start import start_router
from app.database.db import init_db
from app.utils.logger import the_logger
# from app.middlewares.users_middlewares import UserRegistrationMiddleware

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    the_logger.info("Bot started")
    # dp.setup_middleware(UserRegistrationMiddleware())
    dp.include_router(router=start_router)
    dp.include_router(router=order_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    init_db()
    asyncio.run(main())
