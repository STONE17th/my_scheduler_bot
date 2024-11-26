from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from classes import Month, Day
from data_base import DataBase
from handlers.callback import target_day
from keyboards import CallBackData, ikb_cancel, ikb_day_button
from .states import CallbackState

router = Router()


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
    day = Day.from_callback_data(callback_data)
    await state.set_state(CallbackState.input_data)
    await state.update_data(
        **day.as_dict,
        message_id=callback.message.message_id,
    )
    await bot.edit_message_text(
        f'{day.day} {Month.months[day.month]} {day.year}\nВведите время и описание мероприятия:',
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=ikb_cancel(
            target_day=day,
        )
    )


@router.message(CallbackState.input_data)
async def new_task_input(message: Message, state: FSMContext, bot: Bot) -> None:
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    if validate_data := _validate_task(message_data=message.text):
        time, desc = validate_data
        data = await state.get_data()
        user_tg_id, year, month, day, message_id = data['user_tg_id'], data['year'], data['month'], data['day'], data[
            'message_id']
        DataBase().add_task(user_tg_id, year, month, day, time, desc)
        day = Day(user_tg_id, year, month, day)
        await bot.edit_message_text(
            **day.tasks_caption(marker='⊳'),
            chat_id=message.chat.id,
            message_id=message_id,
            reply_markup=ikb_day_button(
                target_day=day,
                admin=message.from_user.id == user_tg_id,
            ),
        )


@router.callback_query(CallBackData.filter(F.button == 'cancel'))
@router.callback_query(CallbackState.input_data, CallBackData.filter(F.button == 'cancel'))
async def cancel_handler(callback: CallbackQuery, callback_data: CallBackData, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    await target_day(callback, callback_data, bot)
