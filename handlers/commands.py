from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from classes import Amount, Month, Day
from data_base import DataBase
from fsm.states import CallbackState
from middlewares import DateMiddleware
from keyboards import ikb_current_month, ikb_day_button

command_router = Router()

command_router.message.middleware(DateMiddleware())


@command_router.message(Command('start'))
@command_router.message(Command('start'), CallbackState())
async def command_start(message: Message, state: FSMContext, current_year: int, current_month: int):
    await state.clear()
    msg = f'Приветствую, {message.from_user.full_name}!'
    user_tg_id = message.from_user.id
    if message.forward_origin:
        user_tg_id = message.forward_origin.sender_user.id
        msg += f'''\nСохрани ссылку для быстрого перехода:
        https://t.me/stone_scheduler_bot?start={message.forward_origin.sender_user.id}'''
    if message.text != '/start' and message.text.split()[-1].isdigit():
        user_tg_id = int(message.text.split()[-1])
    msg += '\nВыбери день:'
    DataBase().create_user_table(user_tg_id)
    await message.answer(
        text=msg,
        reply_markup=ikb_current_month(
            user_tg_id,
            current_year,
            current_month,
        )
    )


@command_router.message(F.forward_origin)
async def forward_handler(message: Message, bot: Bot):
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    await command_start(message)


@command_router.message(Command('load'))
async def add_task(message: Message, bot: Bot, command: CommandObject):
    with open(command.args, 'r', encoding='utf-8') as file:
        data = list(map(lambda x: x.strip().split(' - '), file.readlines()))
    for row in data:
        day, month, year = map(int, row[0].split('.'))
        DataBase().add_task(message.from_user.id, year, month, day, row[1], row[2])


@command_router.message(Command('count'))
async def count_tasks(message: Message, bot: Bot, command: CommandObject):
    year, month, text = command.args.split(' ', 2)
    tasks = DataBase().count_tasks(message.from_user.id, int(year), int(month))
    await message.answer(str(len([task for task in tasks if text.lower() in task[-1].lower()])))


@command_router.message()
async def go_to_date(message: Message, bot: Bot, current_year: int, current_month: int):
    date = message.text.split()
    day, month, year = None, current_month, current_year
    await bot.delete_message(
        chat_id=message.from_user.id,
        message_id=message.message_id,
    )
    if all(map(lambda x: x.isdigit(), date)):
        date = tuple(map(int, date))
        match date:
            case [day]:
                if 1 <= day <= Month(year, month).day_amount():
                    day = day
            case [day, month]:
                if Amount.MIN_MONTH.value <= month <= Amount.MAX_MONTH.value:
                    if 1 <= day <= Month(year, month).day_amount():
                        day, month = day, month
            case [day, month, year]:
                if Amount.MIN_MONTH.value <= month <= Amount.MAX_MONTH.value:
                    if 1 <= day <= Month(year, month).day_amount():
                        if len(str(year)) in (2, 4):
                            if len(str(year)):
                                year += 2000
                            day, month, year = day, month, year
        if day is None:
            msg = '\nВыбери день:'
            await message.answer(
                text=msg,
                reply_markup=ikb_current_month(
                    message.from_user.id,
                    current_year,
                    current_month,
                )
            )
        else:
            day = Day(
                message.from_user.id,
                year,
                month,
                day,
            )
            await bot.send_message(
                **day.tasks_caption(),
                chat_id=message.from_user.id,
                reply_markup=ikb_day_button(
                    target_day=day,
                    admin=True,
                ),
            )
