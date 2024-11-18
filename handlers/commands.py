from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject

from datetime import datetime

from data_base import Schedule
from keyboards import ikb_current_month

command_router = Router()


@command_router.message(CommandStart)
async def command_start(message: Message, command: CommandObject):
    print(command.args)
    # msg = message.text.split()
    # if len(msg) == 2 and msg[1].isdigit():
    #     user_tg_id = int(msg[1])
    # else:
    #     user_tg_id = message.from_user.id
    # Schedule().create_user_table(message.from_user.id)
    # today_date = datetime.now()
    # year = today_date.year
    # month = today_date.month
    # await message.answer(
    #     message.text,
    #     reply_markup=ikb_current_month(
    #         user_tg_id,
    #         year,
    #         month,
    #     )
    # )


# @command_router.message(Command('del'))
# async def command_start(message: Message):
#     Schedule().del_task(message.from_user.id, 1)
#     await message.answer(
#         'Удалено'
#     )
