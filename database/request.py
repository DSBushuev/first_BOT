from sqlalchemy import select, update, delete
from database.models import async_session
from database.models import User, Item, Category


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()

async def get_categores():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_category_items(category_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category == int(category_id)))
    
async def get_category_by_item(item_id):
    async with async_session() as session:
        result = await session.execute(
            select(Item).where(Item.id == item_id)
        )
        item = result.scalar_one_or_none()
        return item.category

async def get_description(item_id):
     async with async_session() as session:
        result = await session.execute(
            select(Item).where(Item.id == item_id)
        )
        item = result.scalar_one_or_none()
        return item.description