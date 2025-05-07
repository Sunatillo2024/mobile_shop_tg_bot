from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍️ View Products"), KeyboardButton(text="🛒 My Cart")],
            [KeyboardButton(text="📦 My Orders"), KeyboardButton(text="📍 My Address")],
            [KeyboardButton(text="☎️ Contact Support")]
        ],
        resize_keyboard=True
    )
    return keyboard
