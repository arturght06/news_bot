from telethon.sync import TelegramClient

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from config import *


tg_client = TelegramClient(phone, api_id, api_hash)

tg_client.start()


# object of channel data from row telethon object to json dictionary
# class TgChannelObject:
#     def __init__(self, chat):
#         self.channel_id = None
#         self.channel_username = None
#         self.channel_title = None
#         self.channel_logo_id = None
#         self.channel_verified = None
#         self.channel_has_link = None
#         self.channel_access_hash = None
#         self.channel_subs = None
#
#         if hasattr(chat, "id"):
#             self.channel_id = chat.id
#         if hasattr(chat, "username"):
#             self.channel_username = chat.username
#         if hasattr(chat, "title"):
#             self.channel_title = chat.title
#         if hasattr(chat, "photo.photo_id"):
#             self.channel_logo_id = chat.photo.photo_id
#         if hasattr(chat, "verified"):
#             self.channel_verified = chat.verified
#         if hasattr(chat, "has_link"):
#             self.channel_has_link = chat.has_link
#         if hasattr(chat, "access_hash"):
#             self.channel_access_hash = chat.access_hash
#         if hasattr(chat, "participants_count"):
#             self.channel_subs = chat.participants_count
#
#         self.json_dict = {
#             "id": self.channel_id,
#             "access_hash": self.channel_access_hash,
#             "username": self.channel_username,
#             "title": self.channel_title,
#             "logo_id": self.channel_logo_id,
#             "verified": self.channel_verified,
#             "has_link": self.channel_has_link,
#             "count_subs": self.channel_subs
#         }
#
#     # return json dictionary data of object
#     def json(self):
#         return self.json_dict


# the main parser class contains all functions for parsing channels, data, posts etc.
# also contains telethon client for parsing
class Parser:
    def __init__(self, tg_client):
        self.client = tg_client
        self.channels = []
        self.last_date = None

    def get_channels(self):
        result = self.client.iter_dialogs()

        for row_channel in result:
            if not row_channel.is_group and row_channel.is_channel:
                channel_data = {
                    "id": row_channel.entity.id,
                    "access_hash": row_channel.entity.access_hash,
                    "username": row_channel.entity.username,
                    "title": row_channel.name,
                    "subscribers_count": row_channel.entity.participants_count,
                    "creation_date": row_channel.name,
                    "has_link": row_channel.entity.has_link,
                    "join_request": row_channel.entity.join_request,
                    "last_post": {
                        "id": row_channel.message.id,
                        "time": row_channel.message.date,
                        "text": row_channel.message.message,
                    },
                }
            else:
                continue

            # for i in row_channel:
            #     print(i)

            self.channels.append(channel_data)

        return self.channels


parser = Parser(tg_client)
parser.get_channels()

print(parser.channels)

for channel in parser.channels:
    print(channel)

# print(groups)

