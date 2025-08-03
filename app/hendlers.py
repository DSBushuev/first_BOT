from aiogram import types, filters, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import database.request as rq
from database.request import get_description

router = Router()

@router.message(filters.CommandStart())
async def cmd_start(message:types.Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f"Твой Telegram ID: {message.from_user.id}")
    #await message.reply(f"Добро пожаловать в телеграмм-магазин кросовок", reply_markup=kb.main)


@router.message(F.text == 'Catalog')
async def catalog(message:types.Message):
    await message.answer("Выберете категорию товара", reply_markup=await kb.categories())

@router.callback_query(F.data == 'Catalog')
async def catalog(callback:types.CallbackQuery):
    await callback.message.edit_text("Выберете категорию товара", reply_markup=await kb.categories())

@router.callback_query(F.data.startswith('category_'))
async def category(callback:types.CallbackQuery):
    await callback.message.edit_text(f"Выберете модель {callback.data.split('_')[1]}")
    await callback.message.edit_reply_markup(reply_markup=await kb.items_by_category(int(callback.data.split('_')[1])))

@router.callback_query(F.data.startswith('item_'))
async def item(callback:types.CallbackQuery):
    item_description = await get_description(int(callback.data.split('_')[1]))
    await callback.message.edit_text(f"Вы выбрали модель {item_description}")
    await callback.message.edit_reply_markup(reply_markup=await kb.item(int(callback.data.split('_')[1])))
