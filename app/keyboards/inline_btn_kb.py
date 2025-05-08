from aiogram.filters import callback_data
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto

from app.database.crud import get_category_name_from_db


async def Show_Categories():
    categories = get_category_name_from_db()  # [(id, name), ...]

    # Проверяем данные, чтобы убедиться, что кортежи содержат два элемента
    for category in categories:
        print(category)  # Это отладка

    keyboard = [
        [InlineKeyboardButton(text=category[1], callback_data=f"category_{category[0]}")]
        for category in categories
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def Show_Product_Detail_plus_photo_mines_():
    categories = get_category_name_from_db()
    for category in categories:
        print(category)
        keyboard = [
            [InlineKeyboardButton(text=category[1], callback_data=f"product_{category[0]}")]
            for category in categories

        ]



async def send_product_detail(bot, chat_id, product):
    # Inline keyboard with Plus, Minus, and Add to Cart
    quantity_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➖", callback_data=f"decrease_{product.id}"),
                InlineKeyboardButton(text="1", callback_data="quantity_display"),
                InlineKeyboardButton(text="➕", callback_data=f"increase_{product.id}")
            ],
            [
                InlineKeyboardButton(text="🛒 Add to Cart", callback_data=f"addtocart_{product.id}")
            ]
        ]
    )

    caption = f"📦 <b>{product.name}</b>\n💵 Price: {product.price} 💸\n\n{product.description}"

    try:
        if product.photo_url:
            await bot.send_photo(
                chat_id=chat_id,
                photo=product.photo_url,
                caption=caption,
                reply_markup=quantity_keyboard,
                parse_mode="HTML"
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=caption,
                reply_markup=quantity_keyboard,
                parse_mode="HTML"
            )
    except Exception as e:
        print(f"[Error sending product]: {e}")
        await bot.send_message(chat_id=chat_id, text="⚠️ Error sending product details.")


