from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
                        InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_categories, get_product_by_category


# Клавиатура "Меню"
main_menu = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🗂 Каталог")],
        [KeyboardButton(text="📲 Контакты")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню... ⬇️"
)


# Кнопка для ввода имени клиента
async def clients_name(name):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=name)]],
        resize_keyboard=True,
        input_field_placeholder="Введите имя или выберите ниже...")


# Создание кнопки для ввода номера телефона при РЕГИСТРАЦИИ
async def clients_phone():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="☎️ Поделиться контактом",
        request_contact=True)]],
        resize_keyboard=True,
        input_field_placeholder="Введите номер или выберите ниже ⬇️")


# Клавиатура "Категории товаров"
async def categories_builder():
    keyboard = InlineKeyboardBuilder() # создали клавиатуру
    all_categories = await get_categories()

    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name, # добавляем в клавиатуру кнопки
                                          callback_data=f"category_{category.id}"))
    return keyboard.adjust(2).as_markup()


# Клавиатура "Товаров" и возврата Назад
async def product_builder(category_id):
    keyboard = InlineKeyboardBuilder() # создали клавиатуру
    all_products = await get_product_by_category(category_id)

    for product in all_products:
        keyboard.row(InlineKeyboardButton(text=f"{product.name} | {product.price} RUB",
                                        callback_data=f"product_{product.id}"))
    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="categories"))
    return keyboard.as_markup()


# Создание кнопки Покупки и возврата Назад
async def back_to_categories(category_id, product_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔗 Связаться с изготовителем", callback_data=f"buy_{product_id}")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data=f"category_{category_id}")]
    ])




