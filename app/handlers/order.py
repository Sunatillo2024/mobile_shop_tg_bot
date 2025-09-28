from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from app.database.crud import (
    check_user_in_db, save_user_to_db, get_category_name_from_db,
    get_products_item_from_db, get_product_by_id
)
from app.keyboards.inline_btn_kb import show_categories, product_detail_keyboard
from app.keyboards.replay_btn_kb import get_main_menu

start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: Message):
    """Handle /start command"""
    try:
        user_id = message.from_user.id
        full_name = message.from_user.full_name or "Unknown"

        # Check if user exists
        existing_user = check_user_in_db(user_id)

        if not existing_user:
            # Create new user
            new_user = save_user_to_db(telegram_id=user_id, full_name=full_name)
            if new_user:
                welcome_text = f"👋 Welcome to Mobile Shop, {full_name}!\n\n"
                welcome_text += "🛍️ Browse our products and find the perfect mobile device for you!\n\n"
                welcome_text += "Use the menu below to get started:"
            else:
                welcome_text = "❌ Sorry, there was an error setting up your account. Please try again."
                await message.answer(welcome_text)
                return
        else:
            welcome_text = f"👋 Welcome back, {full_name}!\n\n"
            welcome_text += "🛍️ Ready to shop for mobile devices?\n\n"
            welcome_text += "Use the menu below:"

        await message.answer(welcome_text, reply_markup=await get_main_menu())

    except Exception as e:
        print(f"[Error in start command]: {e}")
        await message.answer(
            "❌ Something went wrong. Please try again later.",
            reply_markup=await get_main_menu()
        )


@start_router.message(F.text == "📱 Products")
async def show_products(message: Message):
    """Show product categories"""
    try:
        categories_keyboard = await show_categories()
        await message.answer(
            "📱 <b>Choose a category:</b>\n\nSelect from our available mobile device categories:",
            reply_markup=categories_keyboard,
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"[Error showing products]: {e}")
        await message.answer("❌ Failed to load categories. Please try again.")


@start_router.callback_query(F.data.startswith("category_"))
async def show_category_products(callback_query: CallbackQuery):
    """Show products in selected category"""
    try:
        category_id = int(callback_query.data.split("_")[1])
        products = get_products_item_from_db(category_id)

        if not products:
            await callback_query.message.edit_text(
                "📱 No products available in this category at the moment.\n\nPlease check back later!",
                reply_markup=await show_categories()
            )
            await callback_query.answer()
            return

        # Show first product
        product = products[0]
        product_text = f"📱 <b>{product.name}</b>\n\n"
        product_text += f"📝 {product.description or 'No description available'}\n\n"
        product_text += f"💰 <b>Price: ${product.price:.2f}</b>\n"
        product_text += f"📦 <b>Available: {product.available} units</b>\n\n"
        product_text += f"Product 1 of {len(products)}"

        # Create keyboard with navigation if multiple products
        keyboard = product_detail_keyboard(product.id, 1)

        if product.image_url:
            try:
                await callback_query.message.delete()
                await callback_query.message.answer_photo(
                    photo=product.image_url,
                    caption=product_text,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
            except:
                await callback_query.message.edit_text(
                    product_text,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
        else:
            await callback_query.message.edit_text(
                product_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )

        await callback_query.answer()

    except (ValueError, IndexError) as e:
        await callback_query.answer("❌ Invalid category!", show_alert=True)
    except Exception as e:
        print(f"[Error showing category products]: {e}")
        await callback_query.answer("❌ Failed to load products!", show_alert=True)


@start_router.callback_query(F.data.startswith(("increase_", "decrease_")))
async def handle_quantity_change(callback_query: CallbackQuery, state: FSMContext):
    """Handle quantity increase/decrease in product view"""
    try:
        action, product_id_str = callback_query.data.split("_", 1)
        product_id = int(product_id_str)

        # Get current quantity from state or default to 1
        data = await state.get_data()
        current_quantity = data.get(f"quantity_{product_id}", 1)

        # Get product to check availability
        product = get_product_by_id(product_id)
        if not product:
            await callback_query.answer("❌ Product not found!", show_alert=True)
            return

        # Update quantity
        if action == "increase":
            if current_quantity < product.available:
                new_quantity = current_quantity + 1
            else:
                await callback_query.answer(f"❌ Maximum {product.available} units available!", show_alert=True)
                return
        else:  # decrease
            if current_quantity > 1:
                new_quantity = current_quantity - 1
            else:
                await callback_query.answer("❌ Minimum quantity is 1!", show_alert=True)
                return

        # Save new quantity to state
        await state.update_data({f"quantity_{product_id}": new_quantity})

        # Update keyboard
        new_keyboard = product_detail_keyboard(product_id, new_quantity)
        await callback_query.message.edit_reply_markup(reply_markup=new_keyboard)
        await callback_query.answer(f"Quantity: {new_quantity}")

    except (ValueError, IndexError):
        await callback_query.answer("❌ Invalid data!", show_alert=True)
    except Exception as e:
        print(f"[Error handling quantity change]: {e}")
        await callback_query.answer("❌ An error occurred!", show_alert=True)


@start_router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback_query: CallbackQuery):
    """Return to categories view"""
    try:
        categories_keyboard = await show_categories()
        await callback_query.message.edit_text(
            "📱 <b>Choose a category:</b>\n\nSelect from our available mobile device categories:",
            reply_markup=categories_keyboard,
            parse_mode="HTML"
        )
        await callback_query.answer()
    except Exception as e:
        print(f"[Error going back to categories]: {e}")
        await callback_query.answer("❌ An error occurred!", show_alert=True)


@start_router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback_query: CallbackQuery):
    """Return to main menu"""
    try:
        await callback_query.message.delete()
        await callback_query.message.answer(
            "🏠 <b>Main Menu</b>\n\nWhat would you like to do?",
            reply_markup=await get_main_menu(),
            parse_mode="HTML"
        )
        await callback_query.answer()
    except Exception as e:
        print(f"[Error going back to menu]: {e}")
        await callback_query.answer("❌ An error occurred!", show_alert=True)