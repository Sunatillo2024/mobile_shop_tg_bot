from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext


class My_address_FSMContext(State):
    name_location = State()
