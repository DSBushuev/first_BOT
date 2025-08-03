from aiogram import types, filters, F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
#import database.request as rq
#from database.request import get_description
import os
from dotenv import load_dotenv

router = Router()

class AddProduct(StatesGroup):
    name = State()
    # Состояния для каждой характеристики
    char_cpu = State()
    char_ram = State()
    char_storage = State()
    char_gpu = State()
    char_screen_diagonal = State()
    char_screen_resolution = State()
    char_matrix_type = State()
    char_os = State()
    char_year = State()
    char_wifi = State()
    # Финальные шаги
    price = State()
    image = State()

@router.message(filters.CommandStart())
async def cmd_start(message:types.Message):
    admin_ids = os.getenv('ADMIN_IDS', '')
    admin_ids_list = list(map(int, admin_ids.split(',')))
    print('5281437455 ',admin_ids, '    ', admin_ids_list[0])
    if message.from_user.id in admin_ids_list:
        await message.answer("Привет, Админ!", reply_markup=kb.admin_menu)
    else:
        #await rq.set_user(message.from_user.id)
        await message.reply(f"Добро пожаловать в телеграмм-магазин кросовок", reply_markup=kb.user_menu)

# hendlers.py

# ... (после класса AddProduct)

# Список характеристик в правильном порядке (название, ключ для сохранения, следующее состояние)
CHARACTERISTICS_FLOW = [
    {'ask': 'Введите модель процессора:', 'key': 'cpu', 'state': AddProduct.char_cpu},
    {'ask': 'Введите объем оперативной памяти (например, 16 ГБ):', 'key': 'ram', 'state': AddProduct.char_ram},
    {'ask': 'Введите объем и тип накопителя (например, SSD 512 ГБ):', 'key': 'storage', 'state': AddProduct.char_storage},
    {'ask': 'Введите модель графического процессора:', 'key': 'gpu', 'state': AddProduct.char_gpu},
    {'ask': 'Введите диагональ экрана (например, 16") empowering:', 'key': 'screen_diagonal', 'state': AddProduct.char_screen_diagonal},
    {'ask': 'Введите разрешение экрана (например, 1920x1200):', 'key': 'screen_resolution', 'state': AddProduct.char_screen_resolution},
    {'ask': 'Введите тип матрицы (например, IPS):', 'key': 'matrix_type', 'state': AddProduct.char_matrix_type},
    {'ask': 'Введите операционную систему (или "без ОС"):', 'key': 'os', 'state': AddProduct.char_os},
    {'ask': 'Введите год релиза:', 'key': 'year', 'state': AddProduct.char_year},
    {'ask': 'Введите стандарт Wi-Fi (например, Wi-Fi 6):', 'key': 'wifi', 'state': AddProduct.char_wifi},
]


# 1. Начало: реакция на кнопку "➕ Добавить товар"
@router.message(F.text == "➕ Добавить товар")
async def add_product_start(message: types.Message, state: FSMContext):
    await state.set_state(AddProduct.name)
    await message.answer("Введите название товара (например, HUAWEI MCLF-X):")

# 2. Получение названия и запуск опроса по характеристикам
@router.message(AddProduct.name)
async def add_product_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    # Запускаем опрос с первой характеристики
    first_char = CHARACTERISTICS_FLOW[0]
    await state.set_state(first_char['state'])
    await message.answer(first_char['ask'])

# 3. УНИВЕРСАЛЬНЫЙ обработчик для ВСЕХ характеристик
@router.message(
    AddProduct.char_cpu, AddProduct.char_ram, AddProduct.char_storage, AddProduct.char_gpu,
    AddProduct.char_screen_diagonal, AddProduct.char_screen_resolution, AddProduct.char_matrix_type,
    AddProduct.char_os, AddProduct.char_year, AddProduct.char_wifi
)
async def add_product_char(message: types.Message, state: FSMContext):
    current_state_str = await state.get_state()
    
    # Находим текущий шаг
    current_step_index = -1
    for i, char in enumerate(CHARACTERISTICS_FLOW):
        if char['state'].state == current_state_str:
            current_step_index = i
            break
            
    # Сохраняем полученные данные
    key_to_save = CHARACTERISTICS_FLOW[current_step_index]['key']
    await state.update_data({key_to_save: message.text})
    
    # Определяем следующий шаг
    next_step_index = current_step_index + 1
    if next_step_index < len(CHARACTERISTICS_FLOW):
        # Если есть еще характеристики, переходим к следующей
        next_char = CHARACTERISTICS_FLOW[next_step_index]
        await state.set_state(next_char['state'])
        await message.answer(next_char['ask'])
    else:
        # Если характеристики закончились, переходим к цене
        await state.set_state(AddProduct.price)
        await message.answer("Все характеристики записаны. Введите цену товара (только цифры):")

# 4. Получение цены и запрос фото (этот обработчик почти не изменился)
@router.message(AddProduct.price)
async def add_product_price(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите цену цифрами.")
        return
    await state.update_data(price=int(message.text))
    await state.set_state(AddProduct.image)
    await message.answer("Цена установлена. Отправьте фотографию товара.")


# 5. Получение фото и завершение
@router.message(AddProduct.image, F.photo)
async def add_product_image(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    # Формируем красивое описание из собранных данных
    char_list = [
        f"<b>Процессор:</b> {data.get('cpu', '-')}",
        f"<b>Оперативная память:</b> {data.get('ram', '-')}",
        f"<b>Накопитель:</b> {data.get('storage', '-')}",
        f"<b>Графика:</b> {data.get('gpu', '-')}",
        f"<b>Экран:</b> {data.get('screen_diagonal', '-')} / {data.get('screen_resolution', '-')}",
        f"<b>Матрица:</b> {data.get('matrix_type', '-')}",
        f"<b>ОС:</b> {data.get('os', '-')}",
        f"<b>Год релиза:</b> {data.get('year', '-')}",
        f"<b>Wi-Fi:</b> {data.get('wifi', '-')}",
    ]
    description_text = "\n".join(char_list)

    # Здесь будет код для сохранения в базу данных
    
    # Отправляем финальное сообщение с фото и всеми данными
    await message.answer_photo(
        photo=message.photo[-1].file_id,
        caption=f"✅ <b>{data['name']}</b>\n\n"
                f"{description_text}\n\n"
                f"<b>Цена:</b> {data['price']} руб.",
        parse_mode='HTML' # Включаем HTML для жирного шрифта
    )
    
    await state.clear()