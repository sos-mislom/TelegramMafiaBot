import asyncio

import config as c
from aiogram import Bot, Dispatcher
from handlers import others
from aiogram.fsm.storage.memory import MemoryStorage
import logging

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    bot = Bot(token=c.TOKEN_TG)
    rooters = [others]

    for root in rooters: 
        dp.include_router(root.router)

    logging.warning("Стартуем!! СТАРТУЕММ!!")
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    

if __name__ == '__main__':
    asyncio.run(main())
