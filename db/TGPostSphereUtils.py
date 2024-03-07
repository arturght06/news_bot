import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import PostRegion
from db.connect import engine


class TGPostSphereUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    async def get(self, post_id: int) -> PostRegion | None:
        async with self.async_session() as session:
            query = select(PostRegion).where(PostRegion.id == post_id)
            answer = await session.execute(query)
            sphere: PostRegion = answer.scalars().first()

        logging.info(f"Got POST region with id: {post_id}")
        return sphere

    async def set(self, post_region: PostRegion) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed POST sphere for id: {post_region.id}")
                await session.merge(post_region)

    async def remove(self, post_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(PostRegion).where(PostRegion.id == post_id)
                await session.execute(query)

    async def all(self) -> dict[int: str]:
        async with self.async_session() as session:
            answer = await session.execute(select(PostRegion))
            data = answer.scalars().all()

        data: dict[int: str] = {post.id: post.region for post in data}

        logging.info("Got all POST`s regions table")
        return data
