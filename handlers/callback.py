from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.formatting import as_list, as_marked_section
from collections import namedtuple

from classes import Month, Day
from data_base import DataBase
from keyboards import CallBackData, ikb_day_button, ikb_current_month, ikb_select_month

callback_router = Router()


def cb_adapter(cb: CallBackData) -> tuple[int, ...]:
    return cb.user_tg_id, cb.year, cb.month, cb.day, cb.task_id


async def send_tasks_message(user_tg_id: int, t_day: Day, bot: Bot, message_chat_id: int, message_id: int,
                             user_id: int):
    # message_list = [f'{t_day.day} {Month.months[int(t_day.month)]} {t_day.year}']
    # if tasks := t_day.tasks:
    #     for task in sorted(tasks, key=lambda x: x.time):
    #         msg = f'\t{task.time} - {task.description}'
    #         message_list.append(msg)
    # else:
    #     message_list.append('В этот день мероприятий нет')
    # caption = as_list(
    #     as_marked_section(
    #         *message_list,
    #         marker='\t⊳ ',
    #     )
    # )
    # ⇨
    await bot.edit_message_text(
        **t_day.tasks_caption('⊳').as_kwargs(),
        chat_id=message_chat_id,
        message_id=message_id,
        reply_markup=ikb_day_button(
            user_tg_id,
            t_day.year,
            t_day.month,
            t_day.day,
            t_day.is_busy,
            user_id == user_tg_id,
        ),
    )


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
    # await send_tasks_message(
    #     user_tg_id=user_tg_id,
    #     t_day=t_day,
    #     bot=bot,
    #     message_chat_id=callback.message.chat.id,
    #     message_id=callback.message.message_id,
    #     user_id=callback.from_user.id,
    # )
    await bot.edit_message_text(
        **t_day.tasks_caption('⊳').as_kwargs(),
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_day_button(
            user_tg_id,
            year,
            month,
            day,
            t_day.is_busy,
            callback.from_user.id == user_tg_id,
        ),
    )
    # message_list = [f'{day} {Month.months[int(month)]} {year}']
    # free_day = True
    # if tasks := t_day.tasks:
    #     for task in sorted(tasks, key=lambda x: x.time):
    #         msg = f'\t{task.time} - {task.description}'
    #         message_list.append(msg)
    #         free_day = False
    # else:
    #     message_list.append('В этот день мероприятий нет')
    # caption = as_list(
    #     as_marked_section(
    #         *message_list,
    #         marker='\t⊳ ',
    #     )
    # )
    # # ⇨
    # await bot.edit_message_text(
    #     **caption.as_kwargs(),
    #     chat_id=callback.message.chat.id,
    #     message_id=callback.message.message_id,
    #     reply_markup=ikb_day_button(
    #         user_tg_id,
    #         year,
    #         month,
    #         day,
    #         free_day,
    #         callback.from_user.id == user_tg_id,
    #     ),
    # )


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

# @router.callback_query(CallBackData.filter(F.button == 'delete_tasks'))
# async def delete_task(callback: CallbackQuery, callback_data: CallBackData, bot: Bot) -> None:
#     user_tg_id, year, month, day = callback_data.user_tg_id, callback_data.year, callback_data.month, callback_data.day
#     # await state.update_data(
#     #     user_tg_id=user_tg_id,
#     #     **Month(year, month).as_dict(day),
#     # )
#     response_db = DataBase().get_day(user_tg_id, year, month, day)[0]
#     task_id, *_, time, desc = response_db
#     await bot.edit_message_text(
#         f'{day} {Month.months[month]} {year}\nВыберите время мероприятия, которое хотите удалить:',
#         chat_id=callback.message.chat.id,
#         message_id=callback.message.message_id,
#         reply_markup=ikb_list_delete_tasks(user_tg_id, year, month, day)
