from aiogram import types, filters, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
#import database.request as rq
#from database.request import get_description
import os
from dotenv import load_dotenv

router = Router()

@router.message(filters.CommandStart())
async def cmd_start(message:types.Message):
    if message.from_user.id in os.getenv('ADMIN_IDS'):
        await message.answer("Привет, Админ!", reply_markup=kb.admin_menu)
    else:
        #await rq.set_user(message.from_user.id)
        await message.reply(f"Добро пожаловать в телеграмм-магазин кросовок", reply_markup=kb.user_menu)

