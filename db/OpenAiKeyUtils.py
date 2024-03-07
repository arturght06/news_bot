import logging
from datetime import timedelta
import time
import random
from typing import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import OpenAiKey
from db.connect import engine


class OpenAiKeyUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    async def get(self, key: str) -> OpenAiKey | None:
        async with self.async_session() as session:
            query = select(OpenAiKey).where(OpenAiKey.key == key)
            answer = await session.execute(query)
            post_data: OpenAiKey = answer.scalars().first()

        logging.info(f"Got data for OpenAi_KEY: {str(key)[:8]}")
        return post_data

    async def set(self, key_data: OpenAiKey) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed OpenAi_KEY data: {str(key_data.key)[:8]}")
                await session.merge(key_data)

    async def remove(self, key: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(OpenAiKey).where(OpenAiKey.key == key)
                await session.execute(query)

    async def all(self) -> dict[int: OpenAiKey]:
        async with self.async_session() as session:
            answer = await session.execute(select(OpenAiKey))
            data = answer.scalars().all()

        data: dict[str: OpenAiKey] = {key.key: key for key in data}

        logging.info("Got all OpenAi_KEY`S table")
        return data

    async def get_with_filters(self, unusable: bool = False, last_taking_time: int = 0):
        query = select(OpenAiKey)
        query = query.where(OpenAiKey.unusable == unusable)

        if last_taking_time != 0:
            query = query.where(OpenAiKey.taking_time <= last_taking_time)

        async with self.async_session() as session:
            answer = await session.execute(query)
            post_data: Sequence[OpenAiKey] = answer.scalars().all()

        logging.info("Got KEY`s with filters")
        return post_data

    async def get_fresh_key(self, time_since_last_taking: int = 23):
        time_since_last_taking: int = int(time.time() - time_since_last_taking)

        available_keys = await self.get_with_filters(last_taking_time=time_since_last_taking)
        if len(available_keys) == 0:
            return None
        random_key: OpenAiKey = random.choice(available_keys)
        new_time = OpenAiKey(key=random_key.key, taking_time=time.time())
        await self.set(new_time)
        return random_key.key






