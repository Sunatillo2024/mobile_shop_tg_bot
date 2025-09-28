import asyncio
import sys
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import dp, TOKEN
from app.handlers.order import order_router
from app.handlers.start import start_router, cart_router
from app.database.db import init_db, test_connection
from app.utils.logger import the_logger


async def on_startup():
    """Initialize bot on startup"""
    try:
        the_logger.info("🚀 Starting Mobile Shop Bot...")

        # Test database connection
        if not test_connection():
            the_logger.error("❌ Database connection failed! Please check your DATABASE_URL.")
            sys.exit(1)

        # Initialize database
        if not init_db():
            the_logger.error("❌ Database initialization failed!")
            sys.exit(1)

        the_logger.info("✅ Bot initialization completed successfully!")

    except Exception as e:
        the_logger.error(f"❌ Startup failed: {e}")
        sys.exit(1)


async def on_shutdown():
    """Cleanup on shutdown"""
    the_logger.info("🛑 Shutting down Mobile Shop Bot...")


async def main() -> None:
    """Main bot function"""
    try:
        # Validate token
        if not TOKEN:
            the_logger.error("❌ BOT_TOKEN not found in environment variables!")
            sys.exit(1)

        # Create bot instance
        bot = Bot(
            token=TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

        # Register startup/shutdown handlers
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)

        # Include routers
        dp.include_router(start_router)
        dp.include_router(cart_router)
        dp.include_router(order_router)

        the_logger.info("🤖 Bot is starting polling...")

        # Start polling
        await dp.start_polling(
            bot,
            skip_updates=True,  # Skip pending updates
            allowed_updates=["message", "callback_query", "inline_query"]
        )

    except KeyboardInterrupt:
        the_logger.info("🛑 Bot stopped by user")
    except Exception as e:
        the_logger.error(f"❌ Bot error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        the_logger.info("👋 Bot stopped gracefully")
    except Exception as e:
        the_logger.error(f"❌ Fatal error: {e}")
        sys.exit(1)