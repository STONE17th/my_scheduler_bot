from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from datetime import datetime

from classes import Month
from keyboards import CallBackData


class DateMiddleware(BaseMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],
                       ) -> Any:
        today_date = datetime.now()
        data['current_year'] = today_date.year
        data['current_month'] = today_date.month
        return await handler(event, data)


class MonthClass(BaseMiddleware):

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],
                       ) -> Any:
        cb_data: CallBackData = data['callback_data']
        print('Inner middleware')
        target_month = Month(cb_data.year, cb_data.month)
        data['target_month'] = target_month
        return await handler(event, data)
