from datetime import datetime
from typing import Tuple, Any, List


class Day:
    pass


class Month:
    months = (
        'название месяцев',
        'январь',
        'февраль',
        'март',
        'апрель',
        'май',
        'июнь',
        'июль',
        'август',
        'сентябрь',
        'октябрь',
        'ноябрь',
        'декабрь',
    )

    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month

    @property
    def first_day(self):
        return datetime.strptime(
            f'{self.year}/{self.month}/01',
            "%Y/%m/%d").weekday()

    def _is_leap(self):
        return bool(not self.year % 4 and self.year % 100 or not self.year % 400)

    @property
    def day_amount(self):
        months = {
            1: 31,
            2: 29 if self._is_leap() else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
        return months[self.month]

    def month_calendar(self) -> tuple[Any, tuple[tuple[int, ...] | list[int] | tuple, ...]]:
        calendar = []
        week = [0] * self.first_day
        for day_number in range(1, self.day_amount + 1):
            if len(week) >= 7:
                calendar.append(tuple(week))
                week = []
            week.append(day_number)
        calendar.append(week)
        while len(calendar[-1]) % 7:
            calendar[-1] += [0]
        calendar[-1] = tuple(calendar[-1])
        return Month.months[self.month], tuple(calendar)
