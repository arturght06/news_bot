from sqlalchemy import BigInteger

from TextManager import channels_to_table, channel_to_table, keys_to_table
from create_bot import bot, dp, tg_channels_manager, parser_main, openai_key_manager
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard import greet_key, admin_main_keyboard, admin_key

from config import admin_id
from db.models import TgChannel, OpenAiKey


class FSMcreate(StatesGroup):
    admin_start: State = State()


async def admin_start(message: types.Message):
    if message.from_user.id in admin_id:
        await FSMcreate.admin_start.set()
        await bot.send_message(chat_id=message.from_user.id,
                               text="Вітаю👋\nЦе зручна адмін панель в якій ти можеш керувати ботом.\n"
                                    "<code>/unaccepted_channels</code> - show all unaccepted channels\n"
                                    "<code>/accepted_channels</code> - show all accepted channels\n"
                                    "<code>/show <i>id</i></code> - show info of channel\n"
                                    "<code>/recheck</code> - recheck channels at tg account\n"
                                    "<code>/on <i>id</i></code> - confirm channel\n"
                                    "<code>/off <i>id</i></code>  - confirm channel\n",
                               reply_markup=admin_main_keyboard)


async def show_unaccepted_channels(message: types.Message):
    channels: dict = await tg_channels_manager.all(accepted=False)
    text = "🔴 These channels are NOT ACCEPTED:\n\n"
    table = await channels_to_table(channels=channels)
    text = text + f"<code>{table}</code>"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def show_accepted_channels(message: types.Message):
    channels: dict = await tg_channels_manager.all(accepted=True)
    text = "🟢 These channels are ACCEPTED:\n\n"
    table = await channels_to_table(channels=channels)
    text = text + f"<code>{table}</code>"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def add_channel(message: types.Message):
    arguments: str = message.get_args()
    if arguments.isnumeric():
        channel_id: BigInteger = int(arguments)
        channel_data = await tg_channels_manager.get(channel_id=channel_id)
        if channel_data is not None:
            new_data: TgChannel = TgChannel(id=channel_id, accepted=True)
            await tg_channels_manager.set(new_data)
            text = f"Channel {channel_id} confirmed 🟢"
        else:
            text = f"⚠️Channel {channel_id} does not exists in db"
    else:
        text = "⚠️Error was occurred"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def del_channel(message: types.Message):
    arguments: str = message.get_args()
    if arguments.isnumeric():
        channel_id: BigInteger = int(arguments)
        channel_data = await tg_channels_manager.get(channel_id=channel_id)
        if channel_data is not None:
            new_data: TgChannel = TgChannel(id=channel_id, accepted=False)
            await tg_channels_manager.set(new_data)
            text = f"Channel {channel_id} unconfirmed 🔴"
        else:
            text = f"⚠️Channel {channel_id} does not exists in db"
    else:
        text = "⚠️Error was occurred"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def show_channel(message: types.Message):
    arguments: str = message.get_args()
    if arguments.isnumeric():
        channel_id: BigInteger = int(arguments)
        channel_data: TgChannel = await tg_channels_manager.get(channel_id=channel_id)

        if channel_data is not None:
            table: str = await channel_to_table(channel_data)
            text: str = f"👉Channel <b>{channel_data.title}</b>:\n\n" + table
        else:
            text: str = f"⚠️Channel {channel_id} does not exists in db"
    else:
        text: str = "⚠️Error was occurred"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def recheck_channels(message: types.Message):
    await parser_main.add_new_channels()
    await show_unaccepted_channels(message)


async def add_key(message: types.Message):
    arguments: str = message.get_args()
    if isinstance(arguments, str):
        key: str = str(arguments)
        key_data: OpenAiKey = OpenAiKey(key=key)
        await openai_key_manager.set(key_data=key_data)
        text = f"Key {key[:8]} added 🟢"
    else:
        text = "⚠️Error was occurred"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def show_all_keys(message: types.Message):
    keys: dict = await openai_key_manager.all()
    text = "Keys:\n\n"
    table = await keys_to_table(keys=keys)
    text = text + f"<code>{table}</code>"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def del_key(message: types.Message):
    arguments: str = message.get_args()
    if isinstance(arguments, str):
        key: str = str(arguments)
        channel_data = await openai_key_manager.get(key=key)
        if channel_data is not None:
            await openai_key_manager.remove(key=key)
            text = f"Key {key[:8]}... deleted 🔴"
        else:
            text = f"⚠️Key {key[:8]}... does not exists in db"
    else:
        text = "⚠️Error was occurred"
    await bot.send_message(chat_id=message.from_user.id, text=text)


async def back(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    elif str(current_state) in ["FSMcreate:add_user"]:
        await FSMcreate.admin_start.set()
        await bot.send_message(chat_id=message.from_user.id, text='Ok', reply_markup=admin_key)
        return
    else:
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id, text='Ok', reply_markup=greet_key)
        return


def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', text=['Back'])
    dp.register_message_handler(admin_start, commands=["start_admin_panel"], state="*")
    dp.register_message_handler(show_unaccepted_channels, commands=["unaccepted_channels"], state=FSMcreate.admin_start)
    dp.register_message_handler(show_accepted_channels, commands=["accepted_channels"], state=FSMcreate.admin_start)
    dp.register_message_handler(add_channel, commands=["on"], state=FSMcreate.admin_start)
    dp.register_message_handler(del_channel, commands=["off"], state=FSMcreate.admin_start)
    dp.register_message_handler(show_channel, commands=["show"], state=FSMcreate.admin_start)
    dp.register_message_handler(recheck_channels, commands=["recheck"], state=FSMcreate.admin_start)
    dp.register_message_handler(add_key, commands=["add_key"], state=FSMcreate.admin_start)
    dp.register_message_handler(del_key, commands=["del_key"], state=FSMcreate.admin_start)
    dp.register_message_handler(show_all_keys, commands=["keys"], state=FSMcreate.admin_start)


