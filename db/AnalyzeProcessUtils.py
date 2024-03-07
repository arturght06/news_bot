import logging
from typing import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import AnalyzeProcess
from db.connect import engine


class AnalyzeProcessUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    async def get(self, post_id: int) -> AnalyzeProcess | None:
        async with self.async_session() as session:
            query = select(AnalyzeProcess).where(AnalyzeProcess.id == post_id)
            answer = await session.execute(query)
            sphere: AnalyzeProcess = answer.scalars().first()

        logging.info(f"Got Post analyzing process with id: {post_id}")
        return sphere

    async def set(self, processes: AnalyzeProcess) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed POST analyzing process for id: {processes.id}")
                await session.merge(processes)

    async def remove(self, post_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(AnalyzeProcess).where(AnalyzeProcess.id == post_id)
                await session.execute(query)

    async def all(self) -> dict[int: str]:
        async with self.async_session() as session:
            answer = await session.execute(select(AnalyzeProcess))
            data = answer.scalars().all()

        data: dict[int: str] = {post.id: post.__dict__ for post in data}

        logging.info("Got all POST`s process table")
        return data

    async def get_with_filters(self, translate: bool = False, embedding: bool = False, theme_id: bool = False, region: bool = False, theme: bool = False):
        query = select(AnalyzeProcess)
        query = query.where(AnalyzeProcess.translate == translate)
        query = query.where(AnalyzeProcess.embedding == embedding)
        query = query.where(AnalyzeProcess.theme_id == theme_id)
        query = query.where(AnalyzeProcess.theme == theme)
        query = query.where(AnalyzeProcess.region == region)

        async with self.async_session() as session:
            answer = await session.execute(query)
            post_data: Sequence[AnalyzeProcess] = answer.scalars().all()

        logging.info("Got POSTs processes with filters")
        return post_data
