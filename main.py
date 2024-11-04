import os
import asyncio

from aiogram import Bot, Dispatcher

from handlers import all_routers

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(all_routers)


def on_start():
    print('Bot is started...')


def on_shutdown():
    print('Bot is down now!')


async def start_bot():
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
