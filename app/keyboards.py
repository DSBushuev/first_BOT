from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from database.request import get_categores, get_category_by_item, get_category_items

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Catalog")],
    [KeyboardButton(text="корзина"),
    KeyboardButton(text="контакты"),
    KeyboardButton(text="О нас")]], resize_keyboard=True, input_field_placeholder="Выберете пункт меню")

async def categories():
    all_categories = await get_categores()
    keybord = InlineKeyboardBuilder()
    for category in all_categories:
        keybord.add(InlineKeyboardButton(text = category.name, callback_data=f'category_{category.id}'))
    return keybord.adjust(2).as_markup()
        
async def items_by_category(category_id):
    all_items = await get_category_items(category_id)
    keybord = InlineKeyboardBuilder()
    for item in all_items:
        print(item.name)
        keybord.add(InlineKeyboardButton(text = f'{item.name}\n{item.price}', callback_data=f'item_{item.id}'))
    keybord.add(InlineKeyboardButton(text="Назад", callback_data=f'Catalog'))
    return keybord.adjust(2).as_markup()

async def item(item_id):
    item_category = await get_category_by_item(item_id)
    keybord = InlineKeyboardBuilder()
    keybord.add(InlineKeyboardButton(text ='купить', callback_data=f'item_{item_id}'))
    keybord.add(InlineKeyboardButton(text="Назад", callback_data=f'category_{item_category}'))
    return keybord.adjust(2).as_markup()
        