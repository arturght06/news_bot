import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import UserLanguage
from db.connect import engine


class UserLanguageUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    async def get(self, user_id: int) -> UserLanguage | None:
        async with self.async_session() as session:
            query = select(UserLanguage).where(UserLanguage.id == user_id)
            answer = await session.execute(query)
            user_lang_data: UserLanguage = answer.scalars().first()

        logging.info(f"Got USER data for id: {user_id}")
        return user_lang_data

    async def set(self, user_lang_data: UserLanguage) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed UserLanguage data for id: {user_lang_data.id}")
                await session.merge(user_lang_data)

    async def remove(self, user_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(UserLanguage).where(UserLanguage.id == user_id)
                await session.execute(query)

    async def all(self) -> dict[int: UserLanguage.__dict__]:
        async with self.async_session() as session:
            answer = await session.execute(select(UserLanguage))
            data = answer.scalars().all()

        data: dict[int: UserLanguage.__dict__] = {user.id: user.__dict__ for user in data}

        logging.info("Got all UserLanguage table")
        return data
