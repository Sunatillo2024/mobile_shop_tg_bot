from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from app.database.crud import (
    get_cart_items, add_to_cart, update_cart_quantity,
    clear_cart, get_product_by_id
)
from app.keyboards.inline_btn_kb import cart_keyboard, cart_item_keyboard
from app.keyboards.replay_btn_kb import get_main_menu
from app.utils.Memory_abc import CheckoutStates

cart_router = Router()


@cart_router.message(F.text == "🛒 My Cart")
async def show_cart(message: Message):
    """Display user's cart"""
    user_id = message.from_user.id
    cart_items = get_cart_items(user_id)

    if not cart_items:
        await message.answer(
            "🛒 Your cart is empty!\n\nBrowse our products to add items to your cart.",
            reply_markup=get_main_menu()
        )
        return

    cart_text = "🛒 <b>Your Cart:</b>\n\n"
    total_price = 0

    for item in cart_items:
        product = item.product
        if product:
            item_total = product.price * item.quantity
            total_price += item_total

            cart_text += f"📱 <b>{product.name}</b>\n"
            cart_text += f"💰 ${product.price} x {item.quantity} = ${item_total:.2f}\n\n"

    cart_text += f"💵 <b>Total: ${total_price:.2f}</b>"

    await message.answer(cart_text, reply_markup=cart_keyboard(True), parse_mode="HTML")


@cart_router.callback_query(F.data.startswith("addtocart_"))
async def add_product_to_cart(callback_query: CallbackQuery):
    """Add product to cart"""
    try:
        data_parts = callback_query.data.split("_")
        product_id = int(data_parts[1])
        quantity = int(data_parts[2]) if len(data_parts) > 2 else 1

        user_id = callback_query.from_user.id

        # Check if product exists and is available
        product = get_product_by_id(product_id)
        if not product:
            await callback_query.answer("❌ Product not found!", show_alert=True)
            return

        if product.available < quantity:
            await callback_query.answer(f"❌ Only {product.available} items available!", show_alert=True)
            return

        # Add to cart
        if add_to_cart(user_id, product_id, quantity):
            await callback_query.answer(f"✅ {product.name} added to cart!", show_alert=True)
        else:
            await callback_query.answer("❌ Failed to add to cart!", show_alert=True)

    except (ValueError, IndexError) as e:
        await callback_query.answer("❌ Invalid product data!", show_alert=True)
    except Exception as e:
        print(f"[Error adding to cart]: {e}")
        await callback_query.answer("❌ An error occurred!", show_alert=True)


@cart_router.callback_query(F.data.startswith("cart_increase_"))
async def increase_cart_quantity(callback_query: CallbackQuery):
    """Increase quantity of item in cart"""
    try:
        product_id = int(callback_query.data.split("_")[2])
        user_id = callback_query.from_user.id

        # Get current cart item
        cart_items = get_cart_items(user_id)
        current_item = next((item for item in cart_items if item.product_id == product_id), None)

        if current_item:
            # Check availability
            product = get_product_by_id(product_id)
            if product and current_item.quantity < product.available:
                new_quantity = current_item.quantity + 1
                if update_cart_quantity(user_id, product_id, new_quantity):
                    await callback_query.answer("✅ Quantity increased!")
                    # Refresh cart display
                    await show_cart_callback(callback_query)
                else:
                    await callback_query.answer("❌ Failed to update quantity!")
            else:
                await callback_query.answer("❌ Maximum quantity reached!")
        else:
            await callback_query.answer("❌ Item not found in cart!")

    except (ValueError, IndexError):
        await callback_query.answer("❌ Invalid data!")
    except Exception as e:
        print(f"[Error increasing quantity]: {e}")
        await callback_query.answer("❌ An error occurred!")


@cart_router.callback_query(F.data.startswith("cart_decrease_"))
async def decrease_cart_quantity(callback_query: CallbackQuery):
    """Decrease quantity of item in cart"""
    try:
        product_id = int(callback_query.data.split("_")[2])
        user_id = callback_query.from_user.id

        # Get current cart item
        cart_items = get_cart_items(user_id)
        current_item = next((item for item in cart_items if item.product_id == product_id), None)

        if current_item:
            new_quantity = current_item.quantity - 1
            if update_cart_quantity(user_id, product_id, new_quantity):
                if new_quantity == 0:
                    await callback_query.answer("🗑️ Item removed from cart!")
                else:
                    await callback_query.answer("✅ Quantity decreased!")
                # Refresh cart display
                await show_cart_callback(callback_query)
            else:
                await callback_query.answer("❌ Failed to update quantity!")
        else:
            await callback_query.answer("❌ Item not found in cart!")

    except (ValueError, IndexError):
        await callback_query.answer("❌ Invalid data!")
    except Exception as e:
        print(f"[Error decreasing quantity]: {e}")
        await callback_query.answer("❌ An error occurred!")


@cart_router.callback_query(F.data.startswith("cart_remove_"))
async def remove_from_cart(callback_query: CallbackQuery):
    """Remove item from cart"""
    try:
        product_id = int(callback_query.data.split("_")[2])
        user_id = callback_query.from_user.id

        if update_cart_quantity(user_id, product_id, 0):
            await callback_query.answer("🗑️ Item removed from cart!")
            await show_cart_callback(callback_query)
        else:
            await callback_query.answer("❌ Failed to remove item!")

    except (ValueError, IndexError):
        await callback_query.answer("❌ Invalid data!")
    except Exception as e:
        print(f"[Error removing from cart]: {e}")
        await callback_query.answer("❌ An error occurred!")


@cart_router.callback_query(F.data == "clear_cart")
async def clear_user_cart(callback_query: CallbackQuery):
    """Clear all items from cart"""
    user_id = callback_query.from_user.id

    if clear_cart(user_id):
        await callback_query.message.edit_text(
            "🛒 Your cart has been cleared!",
            reply_markup=cart_keyboard(False)
        )
        await callback_query.answer("🗑️ Cart cleared!")
    else:
        await callback_query.answer("❌ Failed to clear cart!")


async def show_cart_callback(callback_query: CallbackQuery):
    """Helper function to refresh cart display in callback"""
    user_id = callback_query.from_user.id
    cart_items = get_cart_items(user_id)

    if not cart_items:
        await callback_query.message.edit_text(
            "🛒 Your cart is empty!",
            reply_markup=cart_keyboard(False)
        )
        return

    cart_text = "🛒 <b>Your Cart:</b>\n\n"
    total_price = 0

    for item in cart_items:
        product = item.product
        if product:
            item_total = product.price * item.quantity
            total_price += item_total

            cart_text += f"📱 <b>{product.name}</b>\n"
            cart_text += f"💰 ${product.price} x {item.quantity} = ${item_total:.2f}\n"
            cart_text += f"➖ ➕ 🗑️\n\n"

    cart_text += f"💵 <b>Total: ${total_price:.2f}</b>"

    await callback_query.message.edit_text(
        cart_text,
        reply_markup=cart_keyboard(True),
        parse_mode="HTML"
    )