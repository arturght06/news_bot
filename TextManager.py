from texttable import Texttable

from db.models import TgChannel, OpenAiKey


async def channels_to_table(channels: dict[int: TgChannel]) -> str:
    no_channels_message = "No channels in DB🙅‍♂️"
    if len(channels) == 0:
        return no_channels_message
    data = [[channel.title, f". {channel.id} ."] for channel in channels.values()]
    table = Texttable()
    table.add_row(["TITLE", "ID"])
    for row in data:
        table.add_row(row)
    return table.draw()


async def channel_to_table(channel: TgChannel):
    channel = channel.__dict__
    channel.pop("_sa_instance_state")
    text = " \n".join([f"<b>{key}</b>:  <code>{value}</code>" for key, value in reversed(channel.items())])
    return text


async def keys_to_table(keys: dict[str: OpenAiKey]) -> str:
    no_channels_message = "No keys in DB🙅‍♂️"
    if len(keys) == 0:
        return no_channels_message
    data = [[str(key.key)[:8], key.unusable] for key in keys.values()]
    table = Texttable()
    table.add_row(["KEY", "No balance"])
    for row in data:
        table.add_row(row)
    return table.draw()
