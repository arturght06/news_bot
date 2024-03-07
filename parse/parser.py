import asyncio
import sys

from telethon.sync import TelegramClient
from telethon.tl.custom.dialog import Dialog
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, Message

from config import *
from db.models import TgChannel
from db.TGPostsUtils import TGPostsUtils

tg_client = TelegramClient(phone, api_id, api_hash)
tg_client.start()


# the main parser class contains all functions for parsing channels, data, posts etc.
# also contains telethon client for parsing
class Parser:
    def __init__(self, tg_client):
        self.client = tg_client
        self.channels: dict[int: TgChannel] = {}
        self.channel_objects: dict[int: Dialog] = {}
        self.last_date = None

    async def renew_channels(self):
        result = self.client.iter_dialogs()

        async for row_channel in result:
            if not row_channel.is_group and row_channel.is_channel:
                channel_id = row_channel.entity.id

                tg_channel: TgChannel = TgChannel(
                    id=channel_id,
                    access_hash=row_channel.entity.access_hash,
                    title=row_channel.name,
                    username=row_channel.entity.username,
                    participants_count=row_channel.entity.participants_count,
                    last_post_id=row_channel.message.id
                )
            else:
                continue

            row_channel: Dialog
            self.channels[channel_id] = tg_channel
            self.channel_objects[channel_id] = row_channel

    async def parse_to_last_post(self, last_post_id: int, channel_id: int) -> dict:
        channel: Dialog = self.channel_objects[channel_id]
        posts: iter = self.client.iter_messages(channel)

        new_messages: dict[int: Message] = {}
        last_post: int = sys.maxsize
        while last_post > last_post_id + 1:
            post: Message = await anext(posts)

            last_post: int = post.id
            new_messages[last_post] = post

        return new_messages
