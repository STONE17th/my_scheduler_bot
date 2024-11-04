from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from classes import Month
from data_base import Schedule
from keyboards import CallBackData, ikb_back_button, ikb_current_month, ikb_select_month

callback_router = Router()


@callback_router.callback_query(CallBackData.filter(F.button == 'select_month'))
async def select_month(callback: CallbackQuery, bot: Bot):
    user_tg_id, year, month, day = (int(item) for item in callback.data.split(':')[2:])
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
async def select_day(callback: CallbackQuery, bot: Bot):
    user_tg_id, year, month, day = (int(item) for item in callback.data.split(':')[2:])
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
async def target_day(callback: CallbackQuery, bot: Bot):
    user_tg_id, year, month, day = (int(item) for item in callback.data.split(':')[2:])
    tasks = sorted(Schedule().get_day(user_tg_id, year, month, day), key=lambda x: list(map(int, x[-2].split(':'))))
    message_text = []
    if tasks:
        for task_id, task_year, task_month, task_day, task_time, task_desc in tasks:
            msg = f'{task_day} {Month.months[task_month]} {task_year} | {task_time} ({task_id})\n{task_desc}'
            message_text.append(msg)
    else:
        message_text = ['В этот день мероприятий нет']
    message_text = '\n\n'.join(message_text)
    await bot.edit_message_text(
        text=message_text,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_back_button(
            user_tg_id,
            year,
            month,
        ),
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'select_from_months'))
async def select_from_months(callback: CallbackQuery, bot: Bot):
    user_tg_id, year, month, day = (int(item) for item in callback.data.split(':')[2:])
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
