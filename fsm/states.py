from aiogram.fsm.state import State, StatesGroup


class CallbackState(StatesGroup):
    input_data = State()
    confirm = State()
