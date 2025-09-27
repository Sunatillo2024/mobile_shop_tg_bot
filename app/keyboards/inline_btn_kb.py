from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.database.crud import get_category_name_from_db


async def show_categories():
    """Display categories as inline keyboard"""
    categories = get_category_name_from_db()

    if not categories:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ No categories available", callback_data="no_categories")]
        ])

    keyboard = []
    for category in categories:
        keyboard.append([InlineKeyboardButton(
            text=f"📱 {category[1]}",
            callback_data=f"category_{category[0]}"
        )])

    keyboard.append([InlineKeyboardButton(text="🔙 Back to Menu", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def product_detail_keyboard(product_id: int, quantity: int = 1):
    """Create keyboard for product details with quantity controls"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data=f"decrease_{product_id}"),
            InlineKeyboardButton(text=str(quantity), callback_data="quantity_display"),
            InlineKeyboardButton(text="➕", callback_data=f"increase_{product_id}")
        ],
        [
            InlineKeyboardButton(text="🛒 Add to Cart", callback_data=f"addtocart_{product_id}_{quantity}")
        ],
        [
            InlineKeyboardButton(text="🔙 Back to Products", callback_data="back_to_categories")
        ]
    ])


def cart_keyboard(has_items: bool = True):
    """Create keyboard for cart management"""
    keyboard = []

    if has_items:
        keyboard.extend([
            [InlineKeyboardButton(text="✅ Proceed to Checkout", callback_data="checkout")],
            [InlineKeyboardButton(text="🗑️ Clear Cart", callback_data="clear_cart")]
        ])

    keyboard.append([InlineKeyboardButton(text="🔙 Back to Menu", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cart_item_keyboard(product_id: int):
    """Create keyboard for individual cart items"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data=f"cart_decrease_{product_id}"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_increase_{product_id}"),
            InlineKeyboardButton(text="🗑️", callback_data=f"cart_remove_{product_id}")
        ]
    ])