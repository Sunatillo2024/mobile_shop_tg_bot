from aiogram.types import Message, CallbackQuery, Location, Contact
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from app.database.crud import (
    save_address, get_user_address, create_order,
    get_user_orders, get_cart_items
)
from app.keyboards.replay_btn_kb import (
    send_my_address, checkout_keyboard, address_keyboard,
    order_confirmation_keyboard, phone_number_keyboard,
    location_keyboard, get_main_menu
)
from app.utils.Memory_abc import AddressStates, CheckoutStates

order_router = Router()


@order_router.message(F.text == "📍 My Address")
async def my_address(message: Message):
    """Show address management options"""
    try:
        user_id = message.from_user.id
        current_address = get_user_address(user_id)

        if current_address:
            address_text = f"📍 <b>Your current address:</b>\n\n{current_address.address_text}\n\n"
            address_text += "You can update your address using the options below:"
        else:
            address_text = "📍 <b>No address set</b>\n\n"
            address_text += "Please set your delivery address using one of the options below:"

        await message.answer(
            address_text,
            reply_markup=await send_my_address(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[Error in my_address]: {e}")
        await message.answer("❌ Failed to load address information. Please try again.")


@order_router.callback_query(F.data == "send_location")
async def request_location(callback_query: CallbackQuery, state: FSMContext):
    """Request user's location"""
    await state.set_state(AddressStates.waiting_for_location)
    await callback_query.message.answer(
        "📍 Please share your location using the button below:",
        reply_markup=location_keyboard()
    )
    await callback_query.answer()


@order_router.callback_query(F.data == "type_address")
async def request_address_text(callback_query: CallbackQuery, state: FSMContext):
    """Request address as text"""
    await state.set_state(AddressStates.waiting_for_address_text)
    await callback_query.message.answer(
        "✏️ Please type your full delivery address:\n\n"
        "Example: 123 Main Street, Apt 4B, New York, NY 10001",
        reply_markup=await get_main_menu()
    )
    await callback_query.answer()


@order_router.message(AddressStates.waiting_for_location, F.location)
async def process_location(message: Message, state: FSMContext):
    """Process received location"""
    try:
        location: Location = message.location
        user_id = message.from_user.id

        # For now, use coordinates as address text
        # In a real app, you might want to reverse geocode this
        address_text = f"Location: {location.latitude}, {location.longitude}"

        if save_address(user_id, address_text, location.latitude, location.longitude):
            await message.answer(
                "✅ Your location has been saved successfully!",
                reply_markup=await get_main_menu()
            )
        else:
            await message.answer(
                "❌ Failed to save your location. Please try again.",
                reply_markup=await get_main_menu()
            )

        await state.clear()

    except Exception as e:
        print(f"[Error processing location]: {e}")
        await message.answer(
            "❌ Failed to process your location. Please try again.",
            reply_markup=await get_main_menu()
        )
        await state.clear()


@order_router.message(AddressStates.waiting_for_address_text, F.text)
async def process_address_text(message: Message, state: FSMContext):
    """Process received address text"""
    try:
        if message.text == "❌ Cancel":
            await message.answer(
                "Address setup cancelled.",
                reply_markup=await get_main_menu()
            )
            await state.clear()
            return

        user_id = message.from_user.id
        address_text = message.text.strip()

        if len(address_text) < 10:
            await message.answer(
                "❌ Address is too short. Please provide a detailed address.",
            )
            return

        if save_address(user_id, address_text):
            await message.answer(
                f"✅ Your address has been saved successfully!\n\n📍 {address_text}",
                reply_markup=await get_main_menu()
            )
        else:
            await message.answer(
                "❌ Failed to save your address. Please try again.",
                reply_markup=await get_main_menu()
            )

        await state.clear()

    except Exception as e:
        print(f"[Error processing address text]: {e}")
        await message.answer(
            "❌ Failed to process your address. Please try again.",
            reply_markup=await get_main_menu()
        )
        await state.clear()


@order_router.message(F.text == "📋 My Orders")
async def show_my_orders(message: Message):
    """Show user's order history"""
    try:
        user_id = message.from_user.id
        orders = get_user_orders(user_id)

        if not orders:
            await message.answer(
                "📋 <b>No orders found</b>\n\n"
                "You haven't placed any orders yet. Browse our products to get started!",
                reply_markup=await get_main_menu(),
                parse_mode="HTML"
            )
            return

        orders_text = "📋 <b>Your Orders:</b>\n\n"

        for order in orders[:5]:  # Show last 5 orders
            status_emoji = {
                "pending": "⏳",
                "confirmed": "✅",
                "shipped": "🚚",
                "delivered": "📦",
                "cancelled": "❌"
            }

            orders_text += f"{status_emoji.get(order.status, '📋')} <b>Order #{order.id}</b>\n"
            orders_text += f"💰 Total: ${order.total_price:.2f}\n"
            orders_text += f"📅 Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            orders_text += f"📍 Status: {order.status.title()}\n\n"

        if len(orders) > 5:
            orders_text += f"... and {len(orders) - 5} more orders"

        await message.answer(orders_text, parse_mode="HTML")

    except Exception as e:
        print(f"[Error showing orders]: {e}")
        await message.answer("❌ Failed to load your orders. Please try again.")


@order_router.callback_query(F.data == "checkout")
async def start_checkout(callback_query: CallbackQuery, state: FSMContext):
    """Start checkout process"""
    try:
        user_id = callback_query.from_user.id
        cart_items = get_cart_items(user_id)

        if not cart_items:
            await callback_query.answer("❌ Your cart is empty!", show_alert=True)
            return

        # Calculate total
        total_price = 0
        for item in cart_items:
            if item.product:
                total_price += item.product.price * item.quantity

        # Check address
        address = get_user_address(user_id)
        address_status = "✅ Set" if address else "❌ Not set"

        checkout_text = f"🛒 <b>Checkout Summary</b>\n\n"
        checkout_text += f"💰 <b>Total: ${total_price:.2f}</b>\n"
        checkout_text += f"📍 <b>Delivery Address:</b> {address_status}\n"
        checkout_text += f"📞 <b>Phone Number:</b> ❌ Not provided\n\n"
        checkout_text += "Please complete the required information to place your order."

        await callback_query.message.edit_text(
            checkout_text,
            reply_markup=checkout_keyboard(),
            parse_mode="HTML"
        )
        await callback_query.answer()

    except Exception as e:
        print(f"[Error in checkout]: {e}")
        await callback_query.answer("❌ Checkout failed!", show_alert=True)


@order_router.callback_query(F.data == "set_address")
async def set_checkout_address(callback_query: CallbackQuery, state: FSMContext):
    """Set address during checkout"""
    await callback_query.message.answer(
        "📍 <b>Set Delivery Address</b>\n\nChoose how you want to provide your address:",
        reply_markup=address_keyboard(),
        parse_mode="HTML"
    )
    await callback_query.answer()


@order_router.callback_query(F.data == "add_phone")
async def add_phone_number(callback_query: CallbackQuery, state: FSMContext):
    """Add phone number during checkout"""
    await state.set_state(CheckoutStates.waiting_for_phone)
    await callback_query.message.answer(
        "📞 <b>Add Phone Number</b>\n\nPlease share your phone number for delivery coordination:",
        reply_markup=phone_number_keyboard(),
        parse_mode="HTML"
    )
    await callback_query.answer()


@order_router.message(CheckoutStates.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Process phone number from contact"""
    try:
        contact: Contact = message.contact
        phone_number = contact.phone_number

        # Save phone to state
        await state.update_data(phone_number=phone_number)

        await message.answer(
            f"✅ Phone number saved: {phone_number}",
            reply_markup=await get_main_menu()
        )
        await state.clear()

    except Exception as e:
        print(f"[Error processing phone contact]: {e}")
        await message.answer(
            "❌ Failed to save phone number. Please try again.",
            reply_markup=await get_main_menu()
        )
        await state.clear()


@order_router.message(CheckoutStates.waiting_for_phone, F.text)
async def process_phone_text(message: Message, state: FSMContext):
    """Process phone number as text"""
    try:
        if message.text == "❌ Cancel":
            await message.answer(
                "Phone number setup cancelled.",
                reply_markup=await get_main_menu()
            )
            await state.clear()
            return

        phone_number = message.text.strip()

        # Basic phone validation
        if len(phone_number) < 10:
            await message.answer("❌ Please enter a valid phone number.")
            return

        # Save phone to state
        await state.update_data(phone_number=phone_number)

        await message.answer(
            f"✅ Phone number saved: {phone_number}",
            reply_markup=await get_main_menu()
        )
        await state.clear()

    except Exception as e:
        print(f"[Error processing phone text]: {e}")
        await message.answer(
            "❌ Failed to save phone number. Please try again.",
            reply_markup=await get_main_menu()
        )
        await state.clear()


@order_router.callback_query(F.data == "place_order")
async def place_order(callback_query: CallbackQuery, state: FSMContext):
    """Place the order"""
    try:
        user_id = callback_query.from_user.id

        # Check requirements
        address = get_user_address(user_id)
        if not address:
            await callback_query.answer("❌ Please set your delivery address first!", show_alert=True)
            return

        cart_items = get_cart_items(user_id)
        if not cart_items:
            await callback_query.answer("❌ Your cart is empty!", show_alert=True)
            return

        # Get phone from state if available
        data = await state.get_data()
        phone_number = data.get('phone_number')

        # Create order
        order = create_order(user_id, phone_number)

        if order:
            order_text = f"✅ <b>Order Placed Successfully!</b>\n\n"
            order_text += f"📋 <b>Order ID:</b> #{order.id}\n"
            order_text += f"💰 <b>Total:</b> ${order.total_price:.2f}\n"
            order_text += f"📍 <b>Delivery Address:</b> {order.delivery_address}\n"
            if order.phone_number:
                order_text += f"📞 <b>Phone:</b> {order.phone_number}\n"
            order_text += f"\n🕒 <b>Status:</b> {order.status.title()}\n"
            order_text += "\nThank you for your order! We'll contact you soon with delivery details."

            await callback_query.message.edit_text(
                order_text,
                parse_mode="HTML"
            )

            # Clear state
            await state.clear()

        else:
            await callback_query.answer("❌ Failed to place order. Please try again!", show_alert=True)

    except Exception as e:
        print(f"[Error placing order]: {e}")
        await callback_query.answer("❌ Failed to place order!", show_alert=True)


@order_router.callback_query(F.data == "back_to_cart")
async def back_to_cart(callback_query: CallbackQuery):
    """Return to cart view"""
    from app.handlers.start import show_cart_callback
    await show_cart_callback(callback_query)