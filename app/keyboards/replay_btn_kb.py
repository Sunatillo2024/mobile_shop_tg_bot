from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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