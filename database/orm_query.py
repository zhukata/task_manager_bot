from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User


async def orm_add_user(session: AsyncSession, data: dict):
    obj = User(
        telegram_id=data["telegram_id"],
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
    )
    try:
        print('session_add')
        session.add(obj)
        print('before session_add')
        await session.commit()
    except Exception as e:
        print(f'erorr {e}')

# async def orm_get_Users(session: AsyncSession):
#     query = select(User)
#     result = await session.execute(query)
#     return result.scalars().all()

async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.telegram_id == user_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_update_user(session: AsyncSession, user_id: int, user):
    query = select(User).where(User.telegram_id == user_id).values(
        telegram_id=user["telegram_id"],
        access_token=user["access_token"],
        refresh_token=user["refresh_token"]
        )
    await session.execute(query)
    await session.commit()


async def orm_delete_User(session: AsyncSession, user_id: int):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()