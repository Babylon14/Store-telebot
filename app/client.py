from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.database.requests import set_user, update_user
import app.keyboards as kb

import re  # Импортируем модуль регулярных выражений


client = Router()

# Хэндлер по обработке команды /start
@client.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    is_user = await set_user(message.from_user.id)
    if not is_user:
        await message.answer(f"Добро пожаловать в наш онлайн-магазин! 👋\n" \
                            f"Пожалуйста, пройдите процесс регистрации...\n" \
                            f"Введите ваше имя: ✍️",
                            reply_markup=await kb.clients_name(message.from_user.first_name))
        await state.set_state("reg_name")
    else:
        await message.answer(f"Добро пожаловать в наш онлайн-магазин! 👋\n" \
                            f"Используя кнопки ниже, ознакомьтесь с ассортиментом магазина ⬇️",
                            reply_markup=kb.main_menu)


# Хэндлер по отлавливанию Имени пользователя с валидацией
@client.message(StateFilter("reg_name"))
async def get_reg_name(message: Message, state: FSMContext):
    name = message.text.strip()

    # Проверяем, чтобы имя не было одной буквой
    if len(name) < 2:
        await message.answer("❌ Имя слишком короткое.\n"
                             "Имя должно содержать минимум 2 символа.\n"
                             "Пожалуйста, введите корректное имя: ✍️")
        return

    # Регулярное выражение для валидации имени: буквы (кириллица и латиница), пробелы, дефисы
    if not re.fullmatch(r"[a-zA-Zа-яА-ЯёЁ]+(?:[-\s][a-zA-Zа-яА-ЯёЁ]+)*", name):
        await message.answer("❌ Некорректное имя.\n"
                             "Имя должно содержать только буквы, возможно с пробелами или дефисом.\n"
                             "Пожалуйста, введите корректное имя: ✍️")
        return

    await state.update_data(name=name.title()) # сохраняем имя
    await message.answer("Введите номер телефона: ☎️",
                         reply_markup=await kb.clients_phone())
    await state.set_state("reg_phone") # устанавливаем состояние Номера телефона


# Хэндлер для получения номера телефона через ВСТАВКУ контакта (Telegram гарантирует корректность)
@client.message(F.contact, StateFilter("reg_phone"))
async def get_reg_phone_number(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number) # сохраняем номер телефона
    
    data = await state.get_data() # достаем ВСЮ полученную инфу от пользователя
    await update_user(tg_id=message.from_user.id, name=data["name"], phone_number=data["phone_number"])
    await message.answer(f"✅ Вы были успешно зарегистрированы!\n\n" \
                         f"Добро пожаловать в онлайн-магазин! 👋",
                         reply_markup=kb.main_menu)
    
    await state.clear() # очищаем информацию


# Хэндлер для ввода номера телефона ВРУЧНУЮ с валидацией
@client.message(StateFilter("reg_phone"))
async def get_reg_phone_number(message: Message, state: FSMContext):
    raw_phone = message.text.strip().replace("+", "")

    # Удаляем лишние символы, оставляем только цифры
    digits_only = re.sub(r'\D', '', raw_phone)

    # Проверяем, что это действительно телефонный номер
    if not (8 <= len(digits_only) <= 15):
        await message.answer("❌ Некорректный номер телефона.\n"
                             "Номер должен содержать от 8 до 15 цифр.\n"
                             "Пожалуйста, введите корректный номер: ☎️")
        return

    await state.update_data(phone_number=digits_only) # сохраняем номер телефона
    data = await state.get_data() # достаем ВСЮ полученную инфу от пользователя
    await update_user(tg_id=message.from_user.id, name=data["name"], phone_number=digits_only)
    await message.answer(f"✅ Вы были успешно зарегистрированы!\n\n" \
                         f"Добро пожаловать в онлайн-магазин! 👋",
                         reply_markup=kb.main_menu)
    
    await state.clear() # очищаем информацию


# хендлер по обработке нажатия на кнопку "Каталог" (С возможностью кнопки "Назад")
@client.callback_query(F.data == "categories")
@client.message(F.text == "🗂 Каталог")
async def catalog(event: Message | CallbackQuery): 
    if isinstance(event, Message):  # Если ивент - сообщение
        await event.answer("Выберите категорию товара 🛍",
                            reply_markup=await kb.categories())
    else:
        await event.answer("Вы вернулись назад")
        await event.message.edit_text("Выберите категорию товара 🛍",
                                    reply_markup=await kb.categories())


# хендлер по обработке кнопки "Категории"
@client.callback_query(F.data.startswith("category_"))
async def products(callback: CallbackQuery):
    await callback.answer()
    category_id = callback.data.split("_")[1]
    try:
        await callback.message.edit_text(f"Выберите товар ®️",
                                        reply_markup=await kb.card_builder(category_id))
    except: # Если произошла ошибка
        await callback.message.delete() # Удаляем это сообщение
        await callback.message.answer(f"Выберите товар ®️",
                                        reply_markup=await kb.card_builder(category_id))
        