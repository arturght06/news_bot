import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import PostTheme
from db.connect import engine


class TGPostThemeUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    async def get(self, post_id: int) -> PostTheme | None:
        async with self.async_session() as session:
            query = select(PostTheme).where(PostTheme.id == post_id)
            answer = await session.execute(query)
            theme: PostTheme = answer.scalars().first()

        logging.info(f"Got POST theme with id: {post_id}")
        return theme

    async def set(self, post_theme: PostTheme) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed POST theme for id: {post_theme.id}")
                await session.merge(post_theme)

    async def remove(self, post_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(PostTheme).where(PostTheme.id == post_id)
                await session.execute(query)

    async def all(self) -> dict[int: str]:
        async with self.async_session() as session:
            answer = await session.execute(select(PostTheme))
            data = answer.scalars().all()

        data: dict[int: str] = {post.id: post.theme for post in data}

        logging.info("Got all POST`s THEME table")
        return data
