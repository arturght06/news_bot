import logging
from datetime import timedelta
import time
from typing import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import Post
from db.connect import engine


class TGPostsUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    async def get(self, post_id: int) -> Post | None:
        async with self.async_session() as session:
            query = select(Post).where(Post.id == post_id)
            answer = await session.execute(query)
            post_data: Post = answer.scalars().first()

        logging.info(f"Got POST data with id: {post_id}")
        return post_data

    async def set(self, post_data: Post) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed POST data for id: {post_data.id}")
                await session.merge(post_data)

    async def remove(self, post_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(Post).where(Post.id == post_id)
                await session.execute(query)

    async def all(self) -> dict[int: Post.__dict__]:
        async with self.async_session() as session:
            answer = await session.execute(select(Post))
            data = answer.scalars().all()

        data: dict[int: Post.__dict__] = {post.id: post.__dict__ for post in data}

        logging.info("Got all TG_CHANNEL`S table")
        return data

    async def get_with_filters(self, processed: bool = False, days_since_posted: int = 0):
        query = select(Post)
        query = query.where(Post.processed == processed)

        if days_since_posted != 0:
            posting_time: int = int(time.time() - timedelta(days=days_since_posted).total_seconds())
            query = query.where(Post.creation_time >= posting_time)

        async with self.async_session() as session:
            answer = await session.execute(query)
            post_data: Sequence[Post] = answer.scalars().all()

        logging.info("Got POSTs with these filters: processed: {}, days since posted: {}".format(processed, days_since_posted))
        return post_data



