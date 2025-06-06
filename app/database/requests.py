from app.database.models import async_session, User, Category, Product
from sqlalchemy import select, update


# Создадим функцию нового пользователя, который запрашивается по tg_id
async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()
            return False
        else:
            return True if user.name else False

# Создадим функцию по получению данных от нового пользователя
async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


# Создадим функцию по обновлению данных о пользователе
async def update_user(tg_id, name, phone_number):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(name=name,
                                                                            phone_number=phone_number))
        await session.commit()


# Создадим функцию по получению Категорий товаров из Каталога
async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


# Создадим функцию которая достает карточки товаров по категории
async def get_product_by_category(category_id):
    async with async_session() as session:
        return await session.scalars(select(Product).where(Product.category_id == category_id))


# Создадим функцию которая достает инфо товара по его id
async def get_product(product_id):
    async with async_session() as session:
        return await session.scalar(select(Product).where(Product.id == product_id))
    