from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram import F
from app.database.crud import check_user_in_db, save_user_to_db, get_category_name_from_db, get_products_item_from_db, \
    user_create_or_get
from app.keyboards.inline_btn_kb import Show_Categories, send_product_detail
from app.keyboards.replay_btn_kb import get_main_menu  # Assuming you're using a keyboard for the reply

start_router = Router()

@start_router.message(CommandStart)
async def start(message: Message):
    data = message.from_user
    user = await user_create_or_get(data)  # sync funksiya

    await message.answer(f"Salom, {user.full_name}!" )

