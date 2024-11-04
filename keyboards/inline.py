from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from classes import Month
from data_base import Schedule
from .callback_data import CallBackData


def _previous_month(year: int, month: int):
    if month != 1:
        return year, (month - 1)
    return year - 1, 12


def _next_month(year: int, month: int):
    if month != 12:
        return year, (month + 1)
    return year + 1, 1


def ikb_current_month(user_tg_id: int, year: int, month: int):
    keyboard = InlineKeyboardBuilder()
    month_name, days_buttons = Month(year, month).month_calendar()
    previous_year, previous_month = _previous_month(year, month)
    next_year, next_month = _next_month(year, month)
    keyboard.button(
        text='<<<',
        callback_data=CallBackData(
            button='select_month',
            user_tg_id=user_tg_id,
            year=previous_year,
            month=previous_month,

        ),
    )
    keyboard.button(
        text=f'{month_name}, {year}',
        callback_data=CallBackData(
            user_tg_id=user_tg_id,
            button='select_from_months',
            year=year,
            month=month,
        ),
    )
    keyboard.button(
        text='>>>',
        callback_data=CallBackData(
            button='select_month',
            user_tg_id=user_tg_id,
            year=next_year,
            month=next_month,

        ),
    )
    for week in days_buttons:
        for day_number in week:
            free_day = not bool(Schedule().get_day(user_tg_id, year, month, day_number))
            keyboard.button(
                text=(str(day_number) if free_day else f'!{day_number}!') if day_number else ' ',
                callback_data=CallBackData(
                    button='target_day',
                    user_tg_id=user_tg_id,
                    year=year,
                    month=month,
                    day=day_number,
                ) if day_number else CallBackData(
                    button='empty_day'
                )

            )
    keyboard.adjust(3, *[7] * len(days_buttons))
    return keyboard.as_markup()


def ikb_select_month(user_tg_id: int, year: int, month: int):
    keyboard = InlineKeyboardBuilder()
    for num_month, month_name in enumerate(Month.months[1:], 1):
        keyboard.button(
            text=month_name,
            callback_data=CallBackData(
                button='select_month',
                user_tg_id=user_tg_id,
                year=year,
                month=num_month,
            ),
        )
    keyboard.button(
        text='Назад',
        callback_data=CallBackData(
            button='select_month',
            user_tg_id=user_tg_id,
            year=year,
            month=month,

        ),
    )
    keyboard.adjust(3, 3, 3, 3, 1)
    return keyboard.as_markup()


def ikb_back_button(user_tg_id: int, year: int, month: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Назад',
        callback_data=CallBackData(
            button='select_month',
            user_tg_id=user_tg_id,
            year=year,
            month=month,
        )
    )
    return keyboard.as_markup()
