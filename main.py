import os
import asyncio

from aiogram import Bot, Dispatcher

from data_base import DataBase
from fsm import fsm_router
from handlers import all_routers, all_messages_router

bot = Bot(os.getenv('BOT_TOKEN'))
dp = Dispatcher()

dp.include_routers(
    all_routers,
    fsm_router,
    all_messages_router,
)


def on_start():
    print('Bot is started...')
    print('Connect to DataBase:', end=' ')
    try:
        DataBase().create_main_table()
        print('OK!')
    except Exception as e:
        print('Failure...')
        print(e)
        on_shutdown()


def on_shutdown():
    print('Bot is down now!')


async def start_bot():
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
