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


async def send_my_address():
    # Correct the keyboard creation by explicitly passing the list of buttons
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Send 📍 My Address", request_location=True),
                   KeyboardButton(text="Send 📍 My Address write")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
