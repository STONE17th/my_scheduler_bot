from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from classes import Day
from data_base import DataBase
from keyboards import CallBackData, ikb_day_button, ikb_current_month, ikb_select_month, ikb_list_delete_tasks

callback_router = Router()


@callback_router.callback_query(CallBackData.filter(F.button == 'select_month'))
async def select_month(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    await bot.edit_message_text(
        text='Выбери месяц:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_current_month(
            **callback_data.to_dict(),
        )
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'select_day'))
async def select_day(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    await bot.edit_message_text(
        text='Выбери день:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_current_month(
            **callback_data.to_dict(),
        )
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'target_day'))
async def target_day(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    day = Day(**callback_data.to_dict(day=True))
    await bot.edit_message_text(
        **day.tasks_caption(),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_day_button(
            target_day=day,
            admin=callback.from_user.id == callback_data.user_tg_id,
        ),
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'delete_task'))
async def delete_task(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    DataBase().del_task(callback_data.user_tg_id, callback_data.task_id)
    await target_day(callback, callback_data, bot)


@callback_router.callback_query(CallBackData.filter(F.button == 'select_from_months'))
async def select_from_months(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    await bot.edit_message_text(
        text='Выбери месяц:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_select_month(
            **callback_data.to_dict(),
        )
    )


@callback_router.callback_query(CallBackData.filter(F.button == 'delete_tasks'))
async def delete_task(callback: CallbackQuery, callback_data: CallBackData, bot: Bot) -> None:
    day = Day(**callback_data.to_dict(day=True))
    await bot.edit_message_text(
        **day.tasks_caption(
            title='Выберите мероприятие, которое хотите удалить:',
        ),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_list_delete_tasks(
            class_day=day,
            **callback_data.to_dict(day=True),
        ),
    )
