from aiogram.filters.callback_data import CallbackData


class CallBackData(CallbackData, prefix='CBD'):
    button: str
    user_tg_id: int = 0
    year: int = 0
    month: int = 0
    day: int = 0
    task_id: int = 0

    def to_dict(self, day: bool = False, task_id: bool = False) -> dict[str, int]:
        data = {
            'user_tg_id': self.user_tg_id,
            'year': self.year,
            'month': self.month,
        }
        if day:
            data['day'] = self.day
        if task_id:
            data['task_id'] = self.task_id
        return data
