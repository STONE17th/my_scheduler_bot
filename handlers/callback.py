from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_list, as_marked_section
from collections import namedtuple

from classes import Month
from data_base import DataBase
from keyboards import CallBackData, ikb_day_button, ikb_current_month, ikb_select_month

callback_router = Router()


def cb_adapter(cb: CallBackData) -> tuple[int, ...]:
    return cb.user_tg_id, cb.year, cb.month, cb.day, cb.task_id


@callback_router.callback_query(CallBackData.filter(F.button == 'select_month'))
async def select_month(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    user_tg_id, year, month, day, task = cb_adapter(callback_data)
    await bot.edit_message_text(
        text='Выбери день:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_current_month(
            user_tg_id,
            year,
            month,
        )
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'select_day'))
async def select_day(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    user_tg_id, year, month, day, task = cb_adapter(callback_data)
    await bot.edit_message_text(
        text='Выбери день:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_current_month(
            user_tg_id,
            year,
            month,
        )
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'target_day'))
async def target_day(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    user_tg_id, year, month, day, task = cb_adapter(callback_data)
    tasks = sorted(DataBase().get_day(user_tg_id, year, month, day), key=lambda x: list(map(int, x[-2].split(':'))))
    message_list = [f'{day} {Month.months[int(month)]} {year}']
    free_day = True
    if tasks:
        for task_id, task_year, task_month, task_day, task_time, task_desc in tasks:
            msg = f'\t{task_time} - {task_desc}'
            message_list.append(msg)
            free_day = False
    else:
        message_list.append('В этот день мероприятий нет')
    caption = as_list(
        as_marked_section(
            *message_list,
            marker='\t⊳ ',
        )
    )
    # ⇨
    await bot.edit_message_text(
        **caption.as_kwargs(),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_day_button(
            user_tg_id,
            year,
            month,
            day,
            free_day,
            callback.from_user.id == user_tg_id,
        ),
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'cancel'))
@callback_router.callback_query(CallBackData.filter(F.button == 'select_from_months'))
async def select_from_months(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    user_tg_id, year, month, day, task = cb_adapter(callback_data)
    await bot.edit_message_text(
        text='Выбери месяц:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_select_month(
            user_tg_id,
            year,
            month,
        )
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'delete_task'))
async def delete_task(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    user_tg_id = callback_data.user_tg_id
    task_id = callback_data.task_id
    DataBase().del_task(user_tg_id, task_id)
    await target_day(callback, callback_data, bot)
