from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(text="📱 Смартфоны"))
    builder.add(KeyboardButton(text="💻 Ноутбуки"))
    builder.add(KeyboardButton(text="🎧 Аксессуары"))
    builder.add(KeyboardButton(text="🏠 Бытовая техника"))
    builder.add(KeyboardButton(text="🛒 Корзина"))
    builder.add(KeyboardButton(text="📞 Контакты"))

    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True)