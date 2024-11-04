from aiogram import Router

from .callback import callback_router
from .commands import command_router

all_routers = Router()
all_routers.include_routers(
    command_router,
    callback_router,
)

__all__ = [
    'all_routers',
]
