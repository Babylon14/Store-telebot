from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

import configparser

# Читаем настройки из settings.ini
config = configparser.ConfigParser()
config.read("settings.ini")
db_config = config["Database"]


DATABASE_URL = f"postgresql+asyncpg://{db_config["user"]}:{db_config["password"]}@" \
                f"{db_config["host"]}:{db_config["port"]}/{db_config["database"]}"

# Создаем асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем сессию
async_session = async_sessionmaker(engine)


# Создаем базовый декларативный класс
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Создаем дочерний класс "Клиенты"
class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(length=25), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(length=25), nullable=True)


# Создаем дочерний класс "Категории товаров"
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=25))


# Создаем дочерний класс "Товары"
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=30))
    description: Mapped[str] = mapped_column(String(length=256))
    price: Mapped[int] = mapped_column()
    image: Mapped[str] = mapped_column(String(256))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))


# Создание всех таблиц
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


