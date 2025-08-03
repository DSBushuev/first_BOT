from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
#from database.request import get_categores, get_category_by_item, get_category_items

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Добавить товар"), KeyboardButton(text="Все команды"),],
    [KeyboardButton(text="✏️ Изменить цену"),
    KeyboardButton(text="🗑 Удалить товар"),
    KeyboardButton(text="📦 Показать список")]], resize_keyboard=True, input_field_placeholder="Выберете пункт меню")

user_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="➕ Добавить товар в корзину"), KeyboardButton(text="✏️ Узнать у консультанта что-то важное")],
    [KeyboardButton(text="✏️ Написать отзыв"),
    KeyboardButton(text="Сыграть в твиз"),
    KeyboardButton(text="📦 Показать список всех ноутбуков")]], resize_keyboard=True, input_field_placeholder="Выберете пункт меню")




