from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from classes import Month, Day
from data_base import DataBase
from keyboards import CallBackData, ikb_day_button, ikb_current_month, ikb_select_month, ikb_list_delete_tasks

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
    t_day = Day(user_tg_id, year, month, day)
    await bot.edit_message_text(
        **t_day.tasks_caption('⊳').as_kwargs(),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_day_button(
            t_day,
            callback.from_user.id == user_tg_id,
        ),
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'delete_task'))
async def delete_task(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    user_tg_id = callback_data.user_tg_id
    task_id = callback_data.task_id
    DataBase().del_task(user_tg_id, task_id)
    await target_day(callback, callback_data, bot)


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


@callback_router.callback_query(CallBackData.filter(F.button == 'delete_tasks'))
async def delete_task(callback: CallbackQuery, callback_data: CallBackData, bot: Bot) -> None:
    user_tg_id, year, month, day = callback_data.user_tg_id, callback_data.year, callback_data.month, callback_data.day
    response_db = DataBase().get_day(user_tg_id, year, month, day)[0]
    task_id, *_, time, desc = response_db
    await bot.edit_message_text(
        f'{day} {Month.months[month]} {year}\nВыберите время мероприятия, которое хотите удалить:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_list_delete_tasks(user_tg_id, year, month, day),
    )
