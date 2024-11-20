from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from classes import Month
from data_base import DataBase
from handlers.callback import target_day
from keyboards import CallBackData, ikb_cancel, ikb_day_button, ikb_list_delete_tasks
from .states import CallbackState

router = Router()
db = DataBase()


def _format_time(time: str) -> str:
    if len(time) < 3:
        return time.zfill(2) + ':00'
    return time


@router.callback_query(CallBackData.filter(F.button == 'add_task'))
async def add_task_input(callback: CallbackQuery, callback_data: CallBackData, state: FSMContext, bot: Bot) -> None:
    user_tg_id, year, month, day = callback_data.user_tg_id, callback_data.year, callback_data.month, callback_data.day
    await state.set_state(CallbackState.input_data)
    await state.update_data(
        user_tg_id=user_tg_id,
        year=year,
        month=month,
        day=day,
        message_id=callback.message.message_id,
    )
    await bot.edit_message_text(
        f'{day} {Month.months[month]} {year}\nВведите время и описание мероприятия:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_cancel(user_tg_id, year, month, day)
    )


@router.callback_query(CallBackData.filter(F.button == 'delete_tasks'))
async def add_task_input(callback: CallbackQuery, callback_data: CallBackData, state: FSMContext, bot: Bot) -> None:
    user_tg_id, year, month, day = callback_data.user_tg_id, callback_data.year, callback_data.month, callback_data.day
    await state.set_state(CallbackState.input_data)
    await state.update_data(
        user_tg_id=user_tg_id,
        year=year,
        month=month,
        day=day,
    )
    response_db = DataBase().get_day(user_tg_id, year, month, day)[0]
    task_id, *_, time, desc = response_db
    await bot.edit_message_text(
        f'{day} {Month.months[month]} {year}\nВыберите время мероприятия, которое хотите удалить:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_list_delete_tasks(user_tg_id, year, month, day)
    )


@router.message(CallbackState.input_data)
async def new_task_input(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.set_state(CallbackState.input_data)
    data = await state.get_data()
    time, desc = message.text.split(' ', 1)
    time = _format_time(time)
    user_tg_id, year, month, day, message_id = data['user_tg_id'], data['year'], data['month'], data['day'], data[
        'message_id']
    DataBase().add_task(user_tg_id, year, month, day, time, desc)
    tasks = sorted(DataBase().get_day(user_tg_id, year, month, day), key=lambda x: list(map(int, x[-2].split(':'))))
    message_text = [f'{day} {Month.months[int(month)]} {year}']
    free_day = True
    if tasks:
        for task_id, task_year, task_month, task_day, task_time, task_desc in tasks:
            msg = f'\t{task_time} - {task_desc}'
            message_text.append(msg)
            free_day = False
    else:
        message_text.append('В этот день мероприятий нет')
    message_text = '\n'.join(message_text)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await bot.edit_message_text(
        text=message_text,
        chat_id=message.from_user.id,
        message_id=message_id,
        reply_markup=ikb_day_button(
            user_tg_id,
            year,
            month,
            day,
            free_day,
            message.from_user.id == user_tg_id,
        ),
    )


@router.callback_query(CallbackState.input_data, CallBackData.filter(F.button == 'cancel'))
async def cancel_handler(callback: CallbackQuery, callback_data: CallBackData, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await target_day(callback, callback_data, bot)
