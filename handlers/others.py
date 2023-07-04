from aiogram import Router

from config import Text
from filters.filter import *

router = Router()

router.message.filter(
    IsTextFilter()
)

@router.message(
    TypicalFilter(for_replace=Text.Commands.help)
)
async def help(message: Message):
    """Info via commands"""
    
    await message.answer(Text.HELP)
