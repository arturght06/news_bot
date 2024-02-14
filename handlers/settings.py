import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from keyboard import keyboard_choose_lang
from create_bot import dp, bot, db_client, lang_manager
from aiogram import types, Dispatcher


class FSMcreate(StatesGroup):
    choose_language = State()


async def process_hi_command(message):
    """Start bot, choose language..."""
    await FSMcreate.choose_language.set()
    user_id = message.from_user.id
    user_exist = db_client.user_exists(user_id)

    if not user_exist:
        logging.info("NEW USER id:{}".format(user_id))
        # set user settings for saving to db
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        lang_code = message.from_user.language_code

        user_data = (user_id, username, first_name, last_name, lang_code)

        db_client.add_user(user_data)

        lang_data = [user_id, lang_code, None, None, None]

        db_client.set_user_languages(lang_data)

    user_lang_interface = lang_manager.get_user_interface_language(user_id)

    await bot.send_message(chat_id=user_id, text=lang_manager.phrases[user_lang_interface]["welcome"],
                           reply_markup=keyboard_choose_lang)


async def choose_language(message: types.message, state: FSMContext):
    language = message.data[len("choose_lang_"):]
    print(language)


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text=['Назад'])
    dp.register_message_handler(process_hi_command, commands=["start"], state=None)
    dp.register_callback_query_handler(choose_language, lambda c: c.data.startswith('choose_lang_'),
                                       state=FSMcreate.choose_language)
