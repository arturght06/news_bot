import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import Interests
from db.connect import engine


class UserInterestsUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    # Users Methods
    async def get(self, user_id: int) -> Interests | None:
        async with self.async_session() as session:
            query = select(Interests).where(Interests.user_id == user_id)
            answer = await session.execute(query)

            interests: Interests = answer.scalars().first()
        logging.info(f"Got USER interests for id: {user_id}")
        return interests

    async def set(self, user_interests: Interests) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed USER interests for id: {user_interests.user_id}")
                await session.merge(user_interests)

    async def remove(self, user_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(Interests).where(Interests.user_id == user_id)
                await session.execute(query)

    async def all(self) -> dict[int: Interests.__dict__]:
        async with self.async_session() as session:
            answer = await session.execute(select(Interests))
            data = answer.scalars().all()

        data: dict[int: Interests.__dict__] = {user.id: user.__dict__ for user in data}
        return data
