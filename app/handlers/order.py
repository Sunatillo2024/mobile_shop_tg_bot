from aiogram.types import Message
from aiogram import Router
from aiogram import F
from app.keyboards.replay_btn_kb import send_my_address  # Assuming you're using a keyboard for the reply

order_router = Router()


@order_router.message(F.text == "📍 My Address")
async def my_address(message: Message):
    await message.answer("""
        Send your address using the button below or manually write it and send.
    """, reply_markup=await send_my_address())


@order_router.message(F.text == "Send 📍 My Address write")
async def send_my_address(message: Message):
    await message.answer(text="my code")
