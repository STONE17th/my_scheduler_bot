from aiogram.filters.callback_data import CallbackData


class CallBackData(CallbackData, prefix='CBD'):
    button: str
    user_tg_id: int = 0
    year: int = 0
    month: int = 0
    day: int = 0
    task_id: int = 0
