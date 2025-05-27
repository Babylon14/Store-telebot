from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
                        InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories


# Клавиатура "Меню"
main_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🗂 Каталог")],
        [KeyboardButton(text="📲 Наши контакты")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню... ⬇️"
)


# Кнопка для ввода имени клиента
async def clients_name(name):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=name)]],
                               resize_keyboard=True,
                               input_field_placeholder="Введите имя или выберите ниже...")


# Кнопка для ввода номера телефона клиента
async def clients_phone():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поделиться контактом",
                                                        request_contact=True)]],
                                resize_keyboard=True,
                                input_field_placeholder="Введите номер телефона или поделитесь контактом...")


# Клавиатура "Категории товаров"
async def categories():
    keyboard = InlineKeyboardBuilder() # создали клавиатуру
    all_categories = await get_categories()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, # добавляем в клавиатуру кнопки
                                          callback_data=f"category_{category.id}"))
    return keyboard.adjust(2).as_markup()
