from aiogram.utils.keyboard import InlineKeyboardBuilder

from classes import Month, Day
from data_base import DataBase
from .callback_data import CallBackData


def ikb_current_month(user_tg_id: int, year: int, month: int):
    keyboard = InlineKeyboardBuilder()
    month_class = Month(year, month)
    month_name, days_buttons = month_class.month_calendar(user_tg_id=user_tg_id)
    keyboard.button(
        text='⇦⇦⇦',
        callback_data=CallBackData(
            button='select_month',
            user_tg_id=user_tg_id,
            **month_class.previous_month(),

        ),
    )
    keyboard.button(
        text=f'{month_name}, {year}',
        callback_data=CallBackData(
            button='select_from_months',
            user_tg_id=user_tg_id,
            year=year,
            month=month,
        ),
    )
    keyboard.button(
        text='⇨⇨⇨',
        callback_data=CallBackData(
            button='select_month',
            user_tg_id=user_tg_id,
            **month_class.next_month(),

        ),
    )
    for week in days_buttons:
        for day in week:
            keyboard.button(
                text=' ' if day.is_blank else day.to_str,
                callback_data=CallBackData(
                    button='target_day',
                    user_tg_id=user_tg_id,
                    year=year,
                    month=month,
                    day=day.day,
                ) if not day.is_blank else CallBackData(
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


def ikb_day_button(user_tg_id: int, year: int, month: int, day: int, free_day: bool = False, admin: bool = False):
    keyboard = InlineKeyboardBuilder()
    c_month = Month(year, month)
    keyboard.button(
        text='⇦⇦⇦',
        callback_data=CallBackData(
            button='target_day',
            user_tg_id=user_tg_id,
            **c_month.previous_day(day),
        )
    )
    keyboard.button(
        text='⇨⇨⇨',
        callback_data=CallBackData(
            button='target_day',
            user_tg_id=user_tg_id,
            **c_month.next_day(day),
        )
    )
    if admin:
        keyboard.button(
            text='Добавить',
            callback_data=CallBackData(
                button='add_task',
                user_tg_id=user_tg_id,
                **c_month.as_dict(day),
            )
        )
        if not free_day:
            keyboard.button(
                text='Удалить',
                callback_data=CallBackData(
                    button='delete_tasks',
                    user_tg_id=user_tg_id,
                    **c_month.as_dict(day),
                )
            )
    keyboard.button(
        text='Назад',
        callback_data=CallBackData(
            button='select_month',
            user_tg_id=user_tg_id,
            **c_month.as_dict(day),
        )
    )
    keyboard.adjust(2, 2, 1)
    return keyboard.as_markup()


def ikb_cancel(user_tg_id: int, year: int, month: int, day: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text='Отмена',
        callback_data=CallBackData(
            button='cancel',
            user_tg_id=user_tg_id,
            year=year,
            month=month,
            day=day,
        )
    )
    return keyboard.as_markup()


def ikb_list_delete_tasks(user_tg_id: int, year: int, month: int, day: int):
    keyboard = InlineKeyboardBuilder()
    c_month = Month(year, month)
    response_db = DataBase().get_day(user_tg_id, year, month, day)
    for task in response_db:
        task_id, *_, task_time, _ = task
        keyboard.button(
            text=task_time,
            callback_data=CallBackData(
                button='delete_task',
                user_tg_id=user_tg_id,
                **c_month.as_dict(day),
                task_id=task_id,
            )
        )
    keyboard.button(
        text='Назад',
        callback_data=CallBackData(
            button='cancel',
            user_tg_id=user_tg_id,
            **c_month.as_dict(day),
        )
    )
    return keyboard.as_markup()


def ikb_schedulers_list(admin_tg_id: int):
    schedulers_list = DataBase().load_schedulers(admin_tg_id)
    keyboard = InlineKeyboardBuilder()
    for scheduler_tg_id, scheduler_title in schedulers_list:
        keyboard.button(
            text=scheduler_title,
            callback_data=CallBackData(
                button='select_scheduler',
                user_tg_id=scheduler_tg_id,
            )
        )
