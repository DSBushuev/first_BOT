import asyncio
from aiogram import Bot, Dispatcher
from app.hendlers import router
#from database.models import async_main

import os
from dotenv import load_dotenv

async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN_API'))
    dp = Dispatcher(bot=bot)

    dp.include_router(router=router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        load_dotenv()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("BOT STOP")