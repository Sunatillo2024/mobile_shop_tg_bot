from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def get_main_menu():
    """Create main menu reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Products")],
            [KeyboardButton(text="🛒 My Cart"), KeyboardButton(text="📋 My Orders")],
            [KeyboardButton(text="📍 My Address"), KeyboardButton(text="ℹ️ Help")]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard


async def send_my_address():
    """Create keyboard for address sharing"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Send Location", callback_data="send_location")],
        [InlineKeyboardButton(text="✏️ Type Address Manually", callback_data="type_address")],
        [InlineKeyboardButton(text="🔙 Back to Menu", callback_data="back_to_menu")]
    ])


def checkout_keyboard():
    """Create keyboard for checkout process"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Set Delivery Address", callback_data="set_address")],
        [InlineKeyboardButton(text="📞 Add Phone Number", callback_data="add_phone")],
        [InlineKeyboardButton(text="✅ Place Order", callback_data="place_order")],
        [InlineKeyboardButton(text="🔙 Back to Cart", callback_data="back_to_cart")]
    ])


def address_keyboard():
    """Create keyboard for address options"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📍 Send Location", callback_data="send_location")],
        [InlineKeyboardButton(text="✏️ Type Address", callback_data="type_address")],
        [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_checkout")]
    ])


def order_confirmation_keyboard():
    """Create keyboard for order confirmation"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Confirm Order", callback_data="confirm_order")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_order")],
        [InlineKeyboardButton(text="✏️ Edit Order", callback_data="edit_order")]
    ])


def phone_number_keyboard():
    """Create keyboard for phone number sharing"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Share Phone Number", request_contact=True)],
            [KeyboardButton(text="❌ Cancel")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def location_keyboard():
    """Create keyboard for location sharing"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Share Location", request_location=True)],
            [KeyboardButton(text="❌ Cancel")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )