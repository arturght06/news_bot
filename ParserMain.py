import hashlib
import logging
import asyncio

from telethon.tl.types import Message

from db.models import TgChannel, Post
from parse.parser import Parser, tg_client
from db.TGPostsUtils import TGPostsUtils
from db.TGChannelsUtils import TGChannelsUtils


async def background_parsing():
    parser_main = ParserMain()
    while True:
        await asyncio.sleep(5)
        await parser_main.parse_last_posts()


class ParserMain:
    min_post_length = 10

    def __init__(self):
        self.db_post_manager: TGPostsUtils | None = TGPostsUtils()
        self.parser: Parser | None = Parser(tg_client=tg_client)
        self.db_channels_manager: TGChannelsUtils = TGChannelsUtils()

    async def add_new_channels(self):
        await self.parser.renew_channels()
        channels: dict[int: TgChannel] = self.parser.channels
        for channel in channels.values():
            data_from_db = await self.db_channels_manager.get(channel_id=channel.id)
            if data_from_db is None:
                await self.db_channels_manager.set(channel)
                logging.info(f"channel was added: {channel.title}, {channel.id}")

    # returns channel_id`s that posted new posts
    async def compare_posts_count(self) -> dict:
        await self.parser.renew_channels()
        channels_actual: dict = self.parser.channels
        channels_db: dict = await self.db_channels_manager.all()
        channels: dict = {}
        for channel_id, channel in channels_db.items():
            id_real: int = channels_actual[channel_id].last_post_id
            id_db: int = channel.last_post_id
            if id_real > id_db:
                channels[int(channel_id)] = id_db

        return channels

    async def add_parsed_posts(self, parsed_posts: dict):
        for post_id, message in parsed_posts.items():
            message: Message
            if len(message.message) < self.min_post_length:
                continue
            channel_id = message.peer_id.channel_id
            unique_id = hashlib.md5(f"{channel_id}*{post_id}".encode()).hexdigest()
            creation_time = message.__dict__["date"].timestamp()
            post: Post = Post(
                id=unique_id,
                channel_id=channel_id,
                post_id=post_id,
                text=message.message,
                processed=False,
                creation_time=creation_time
            )
            await self.db_post_manager.set(post)

    async def change_last_post_id(self, channel_id: int, parsed_posts: dict):
        last_post_id: int = max(parsed_posts.keys())
        new_channel_data: TgChannel = TgChannel(id=channel_id, last_post_id=last_post_id)
        await self.db_channels_manager.set(new_channel_data)

    async def parse_last_posts(self):
        channels = await self.compare_posts_count()
        for channel_id, post_id in channels.items():
            parsed_posts: dict = await self.parser.parse_to_last_post(last_post_id=post_id, channel_id=channel_id)

            await self.add_parsed_posts(parsed_posts)
            await self.change_last_post_id(channel_id, parsed_posts)
            # await self.change_last_post_id(parsed_posts)
