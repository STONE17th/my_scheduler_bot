from aiogram import Router

from .fsm import router

fsm_router = Router()
fsm_router.include_router(router)

__all__ = [
    'fsm_router',
]
