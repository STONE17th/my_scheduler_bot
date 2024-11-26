from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from data_base import DataBase
from fsm.states import CallbackState
from middlewares import DateMiddleware
from keyboards import ikb_current_month

command_router = Router()

command_router.message.middleware(DateMiddleware())


@command_router.message(Command('start'))
@command_router.message(Command('start'), CallbackState.input_data)
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
