from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram import F
from app.database.crud import check_user_in_db, save_user_to_db, get_category_name_from_db, get_products_item_from_db
from app.keyboards.inline_btn_kb import Show_Categories, send_product_detail
from app.keyboards.replay_btn_kb import get_main_menu  # Assuming you're using a keyboard for the reply

start_router = Router()


@start_router.message(CommandStart())
async def handle_start(message: Message):
    # Check if the user already exists in the database
    user = check_user_in_db(telegram_id=message.from_user.id)

    if user:
        # If user exists, greet them
        await message.answer(f"👋 Welcome back, {user.full_name}!", reply_markup=get_main_menu())
    else:
        # If user does not exist, save them in the database and greet them
        new_user = save_user_to_db(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
        )

        if new_user:
            # After saving the new user, greet them
            await message.answer(f"👋 Welcome, {new_user.full_name}!", reply_markup=get_main_menu())
        else:
            # In case there's an error saving the user
            await message.answer("❌ An error occurred. Please try again later.")


@start_router.message(F.text == "🛍️ View Products")
async def handle_view_categories(message: Message):
    await message.answer("Categories:", reply_markup=await Show_Categories())



# @start_router.callback_query(F.data.startswith("category_"))
# async def handle_category(callback_query: CallbackQuery):
#     category_data = callback_query.data.split("_")
#     if len(category_data) < 2:
#         await callback_query.answer("Invalid category data!")
#         return
#
#     try:
#         category_id = int(category_data[1])  # Берем ID категории
#         products = get_products_item_from_db(category_id)
#
#         if not products:
#             await callback_query.message.answer("❌ No products found in this category.")
#         else:
#             text = "📦 Products:\n" + "\n".join(f"• {p.name} - ${p.price}" for p in products)
#             await callback_query.message.answer(text)
#
#     except ValueError:
#         await callback_query.answer("Invalid category ID!")
#     except Exception as e:
#         await callback_query.answer(f"Error: {str(e)}")
#
#     await callback_query.answer()
#
#


@start_router.callback_query(lambda c: c.data.startswith("product_"))
async def show_products_by_category(callback_query: CallbackQuery):
    category_id = int(callback_query.data.split("_")[1])
    products = get_products_item_from_db(category_id)

    if not products:
        await callback_query.message.answer("❌ No products found in this category.")
        return

    for product in products:
        await send_product_detail(callback_query.bot, callback_query.from_user.id, product)



