from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import User
from app.keyboards.main_menu import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message, session: AsyncSession):
    # Foydalanuvchini telegram_id orqali qidirish
    user = await session.scalar(
        select(User).where(User.telegram_id == message.from_user.id)
    )

    # Agar yo‘q bo‘lsa – yangi foydalanuvchi yaratamiz
    if not user:
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )
        session.add(user)
        await session.commit()

    # Asosiy menyuni ko‘rsatish
    await message.answer(
        "🛍 Добро пожаловать в наш магазин электроники и аксессуаров!\n\n"
        "Выберите категорию для просмотра товаров:",
        reply_markup=get_main_keyboard()
    )
