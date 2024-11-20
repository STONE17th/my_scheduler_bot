from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import as_list, as_marked_section
from aiogram.fsm.context import FSMContext

from classes import Month, Task
from data_base import DataBase
from handlers.callback import target_day
from keyboards import CallBackData, ikb_cancel, ikb_day_button, ikb_list_delete_tasks
from .states import CallbackState

router = Router()
# db = DataBase()


def _validate_task(message_data: str) -> tuple[str, str] | bool:
    data = message_data.split(' ', 1)
    if len(data) == 2:
        time, description = data
        if time.replace(':', '').isdigit():
            if ':' in time:
                hours, minutes = time.split(':')
            else:
                hours, minutes = time.zfill(0), '00'
            if 0 <= int(hours) < 24 and 0 <= int(minutes) < 60:
                time = f'{hours.zfill(2)}:{minutes.zfill(2)}'
                return time, description
    return False


@router.callback_query(CallBackData.filter(F.button == 'add_task'))
async def add_task_input(callback: CallbackQuery, callback_data: CallBackData, state: FSMContext, bot: Bot) -> None:
    user_tg_id, year, month, day = callback_data.user_tg_id, callback_data.year, callback_data.month, callback_data.day
    await state.set_state(CallbackState.input_data)
    await state.update_data(
        user_tg_id=user_tg_id,
        **Month(year, month).as_dict(day),
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
        **Month(year, month).as_dict(day),
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
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await state.set_state(CallbackState.input_data)
    if validate_data := _validate_task(message_data=message.text):
        time, desc = validate_data
        data = await state.get_data()
        user_tg_id, year, month, day, message_id = data['user_tg_id'], data['year'], data['month'], data['day'], data[
            'message_id']
        DataBase().add_task(user_tg_id, year, month, day, time, desc)
        tasks = sorted([Task(*task) for task in DataBase().get_day(user_tg_id, year, month, day)], key=lambda x: x.time)
        message_text = [f'{day} {Month.months[int(month)]} {year}']
        free_day = True
        if tasks:
            for task in tasks:
                message_text.append(f'{task.time} - {task.description}')
                free_day = False
        else:
            message_text.append('В этот день мероприятий нет')
        caption = as_list(
            as_marked_section(
                *message_text,
                marker='\t⊳ ',
            )
        )
        await bot.edit_message_text(
            **caption.as_kwargs(),
            chat_id=message.from_user.id,
            message_id=message_id,
            reply_markup=ikb_day_button(
                user_tg_id=user_tg_id,
                **Month(year, month).as_dict(day),
                free_day=free_day,
                admin=message.from_user.id == user_tg_id,
            ),
        )


@router.callback_query(CallbackState.input_data, CallBackData.filter(F.button == 'cancel'))
async def cancel_handler(callback: CallbackQuery, callback_data: CallBackData, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await target_day(callback, callback_data, bot)
