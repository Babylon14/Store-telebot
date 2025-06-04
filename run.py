import asyncio
import logging
from aiogram import Bot, Dispatcher

import configparser

from app.client import client
from app.database.models import init_models

# from aiogram.fsm.storage.redis import RedisStorage
# import redis.asyncio as aioredis


# Задаем логирование на уровне инфо
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


config = configparser.ConfigParser()
config.read("settings.ini")

BOT_TOKEN = config["Tokens"]["telebot_token"]


# ТОЧКА ВХОДА:
async def main() -> None:
    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()
    dp.include_router(router=client)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    
    await dp.start_polling(bot)

# функция срабатывает при старте бота
async def startup(dispatcher: Dispatcher):
    await init_models()
    logging.info("Запуск программы...")

# функция срабатывает при выключении бота
async def shutdown(dispatcher: Dispatcher):
    logging.info("Бот остановлен...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Остановка бота")




