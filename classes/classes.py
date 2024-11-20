from datetime import datetime

from dataclasses import dataclass
from enum import Enum

from data_base import DataBase


class Amount(Enum):
    HIGH: int = 31
    LOW: int = 30
    FEB_HIGH: int = 29
    FED_LOW: int = 28
    MIN_MONTH: int = 1
    MAX_MONTH: int = 12
    MIN_DAY: int = 1


@dataclass
class Task:
    id: int
    year: int
    month: int
    day: int
    time: str
    description: str


@dataclass
class Day:
    user_tg_id: int
    year: int
    month: int
    day: int
    is_busy: bool
    emoji_digits = {digit: emoji for digit, emoji in
                    zip(list('0123456789'), ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'])}

    @classmethod
    def blank_day(cls):
        return cls(0, 0, 0, 0, False)

    @property
    def is_blank(self) -> bool:
        return not bool(self.day)

    def _emoji_digits(self) -> str:
        return ''.join([self.emoji_digits[digit] for digit in str(self.day)])

    @property
    def to_str(self):
        return self._emoji_digits() if self.is_busy else str(self.day)


class Month:
    months = (
        'Название месяцев',
        'Январь',
        'Февраль',
        'Март',
        'Апрель',
        'Май',
        'Июнь',
        'Июль',
        'Август',
        'Сентябрь',
        'Октябрь',
        'Ноябрь',
        'Декабрь',
    )

    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month

    @property
    def _first_day(self):
        return datetime.strptime(
            f'{self.year}/{self.month}/01',
            "%Y/%m/%d").weekday()

    @property
    def _is_leap(self):
        return bool(not self.year % 4 and self.year % 100 or not self.year % 400)

    def _day_amount(self, month: int = 0):
        months = {
            1: Amount.HIGH.value,
            2: Amount.FEB_HIGH.value if self._is_leap else Amount.FED_LOW.value,
            3: Amount.HIGH.value,
            4: Amount.LOW.value,
            5: Amount.HIGH.value,
            6: Amount.LOW.value,
            7: Amount.HIGH.value,
            8: Amount.HIGH.value,
            9: Amount.LOW.value,
            10: Amount.HIGH.value,
            11: Amount.LOW.value,
            12: Amount.HIGH.value,
        }
        return months[month if month is None else self.month]

    def as_dict(self, day: int) -> dict[str, int]:
        return {'year': self.year, 'month': self.month, 'day': day}

    def previous_day(self, target_day: int):
        year, month = self.year, self.month
        if target_day == Amount.MIN_MONTH.value:
            if self.month == Amount.MIN_MONTH.value:
                month = Amount.MAX_MONTH.value
                day = self._day_amount(month)
                year -= 1
            else:
                month -= 1
                day = self._day_amount(month)
        else:
            day = target_day - 1
        return {'year': year, 'month': month, 'day': day}

    def next_day(self, target_day: int):
        year, month = self.year, self.month
        if target_day == self._day_amount():
            if self.month == Amount.MAX_MONTH.value:
                day = Amount.MIN_DAY.value
                month = Amount.MIN_MONTH.value
                year += 1
            else:
                day = Amount.MIN_DAY.value
                month += 1
        else:
            day = target_day + 1
        return {'year': year, 'month': month, 'day': day}

    def previous_month(self) -> dict[str, int]:
        if self.month != 1:
            return {'year': self.year, 'month': self.month - 1}
        return {'year': self.year - 1, 'month': 12}

    def next_month(self) -> dict[str, int]:
        if self.month != 12:
            return {'year': self.year, 'month': self.month + 1}
        return {'year': self.year + 1, 'month': 1}

    def month_calendar(self, user_tg_id: int) -> tuple[str, list[list[Day]]]:
        user_days = {day for *_, day, _, _ in DataBase().get_month(user_tg_id, self.year, self.month)}
        calendar = []
        week = [Day.blank_day()] * self._first_day
        for day_number in range(1, self._day_amount() + 1):
            if len(week) >= 7:
                calendar.append(week)
                week = []
            week.append(Day(user_tg_id, self.year, self.month, day_number, day_number in user_days))
        calendar.append(week)
        while len(calendar[-1]) % 7:
            calendar[-1] += [Day.blank_day()]
        return Month.months[self.month], calendar
