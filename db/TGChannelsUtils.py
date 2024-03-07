import logging
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete

from db.models import TgChannel
from db.connect import engine


class TGChannelsUtils:
    def __init__(self):
        self.async_session: async_sessionmaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @staticmethod
    async def exit():
        await engine.dispose()

    async def get(self, channel_id: int) -> TgChannel | None:
        async with self.async_session() as session:
            query = select(TgChannel).where(TgChannel.id == channel_id)
            answer = await session.execute(query)
            channel_data: TgChannel = answer.scalars().first()

        logging.info(f"Got TG_CHANNEL data with id: {channel_id}")
        return channel_data

    async def set(self, tg_channel_data: TgChannel) -> None:
        async with self.async_session() as session:
            async with session.begin():
                logging.info(f"Changed TG_CHANNEL data for id: {tg_channel_data.id}")
                await session.merge(tg_channel_data)

    async def remove(self, channel_id: int) -> None:
        async with self.async_session() as session:
            async with session.begin():
                query = delete(TgChannel).where(TgChannel.id == channel_id)
                await session.execute(query)

    async def all(self, accepted: bool = True) -> dict[int: TgChannel]:
        async with self.async_session() as session:
            query = select(TgChannel).where(TgChannel.accepted == accepted)
            answer = await session.execute(query)
            data = answer.scalars().all()

        data: dict[int: TgChannel] = {channel.id: channel for channel in data}

        logging.info("Got all TG_CHANNEL`S table")
        return data
