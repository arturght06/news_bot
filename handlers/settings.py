import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from keyboard import keyboard_choose_lang, keyboard_countries, keyboard_themes
from create_bot import bot, lang_manager, theme_manager, dp, user_manager, user_lang_manager, db_client, interests_manager
from db.models import User, UserLanguage


class FSMcreate(StatesGroup):
    choose_language: State = State()
    choose_country: State = State()
    choose_themes: State = State()


async def process_hi_command(message, state: FSMContext):
    """Start bot, choose language..."""
    await FSMcreate.choose_language.set()

    user_id: int = message.from_user.id
    # print(await user_lang_manager.remove(user_id))
    # print(await user_manager.remove(user_id))
    # print(await interests_manager.remove(user_id))
    if not await user_manager.exists(user_id):
        logging.info("NEW USER id:{}".format(user_id))
        # set user settings for saving to db
        lang_code: str = message.from_user.language_code
        user_data: User = User(
            id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=lang_code
        )
        await user_manager.set(user_data)

        await lang_manager.set_user_interface_language(user_id=user_id, new_lang=lang_code)

    interface_language = await lang_manager.get_user_interface_language(user_id)
    welcome_text = lang_manager.phrases[interface_language]["welcome"]

    bot_message = await bot.send_message(chat_id=user_id, text=welcome_text, reply_markup=await keyboard_choose_lang())
    bot_message_id = bot_message["message_id"]

    await dp.storage.update_data(chat=user_id, data_to_pass=bot_message_id)


async def choose_language(message: types.message, state: FSMContext):
    await bot.answer_callback_query(message.id)
    await FSMcreate.choose_country.set()

    user_id = message.from_user.id

    if str(message.data).startswith("back_to_"):
        previous_data = dict(await dp.storage.get_data(chat=user_id))["data_to_pass"]

        bot_message_id = previous_data[0]
        language = previous_data[1]

        logging.info(f"User: {user_id} returns to choosing country")

        text = (str(lang_manager.phrases[language]["set_themes"])
                .format(lang_manager.country_to_emoji[language]))

        keyboard = await keyboard_countries(user_id, 2)

        bot_message = await bot.edit_message_text(chat_id=user_id, message_id=bot_message_id, text=text,
                                                  reply_markup=keyboard)
        bot_message_id = bot_message["message_id"]

        await dp.storage.update_data(chat=user_id, data_to_pass=[bot_message_id, language])

    elif str(message.data).startswith("choose_lang_"):
        previous_message_id = dict(await dp.storage.get_data(chat=user_id))["data_to_pass"]

        await bot.delete_message(chat_id=user_id, message_id=previous_message_id)

        language = message.data[len("choose_lang_"):]

        await lang_manager.set_user_interface_language(user_id, language)

        logging.info(f"User: {user_id} set new interface language: {language}")

        text = (str(lang_manager.phrases[language]["first_choosing_theme"])
                .format(lang_manager.country_to_emoji[language]))

        keyboard = await keyboard_countries(user_id, 1)

        bot_message = await bot.send_message(chat_id=user_id, text=text, reply_markup=keyboard)
        bot_message_id = bot_message["message_id"]

        await dp.storage.update_data(chat=user_id, data_to_pass=[bot_message_id, language])


async def choose_themes(message: types.message, state: FSMContext):
    await bot.answer_callback_query(message.id)
    await FSMcreate.choose_themes.set()

    user_id = message.from_user.id
    if str(message.data).startswith("choose_country_"):

        previous_data = dict(await dp.storage.get_data(chat=user_id))["data_to_pass"]

        previous_message_id = previous_data[0]
        language: str = previous_data[1]

        country: str = message.data[len("choose_country_"):]
        marked: dict = await theme_manager.marked_themes(user_id=user_id)

        if marked is None:
            logging.info(f"User id: {user_id} firstly get new interests")
            # set fully new interests firstly
            await theme_manager.set_interests(interests=await theme_manager.first_interests, user_id=user_id)
            # dict format True or False interests marked
            marked: dict = await theme_manager.marked_themes(user_id=user_id)

        keyboard = await keyboard_themes(marked, language, country)

        country_name = lang_manager.country_to_name[language][country] + lang_manager.country_to_emoji[country]
        text = str(lang_manager.phrases[language]["choose_themes"]).format(country_name)

        bot_message = await bot.edit_message_text(chat_id=user_id, message_id=previous_message_id, text=text, reply_markup=keyboard)
        bot_message_id = bot_message["message_id"]

        await dp.storage.update_data(chat=user_id, data_to_pass=[bot_message_id, language])

    elif str(message.data).startswith("choose_theme_"):
        country, key = str(message.data[len("choose_theme_"):]).split("_")
        # define previous id message from bot, language of interface
        previous_data = dict(await dp.storage.get_data(chat=user_id))["data_to_pass"]
        previous_message_id = previous_data[0]
        language = previous_data[1]

        marked: dict = await theme_manager.marked_themes(user_id=user_id)
        marked[country][key] = not (marked[country][key])
        # define specified news category without all
        specific_categories = list(marked[country].values())
        specific_categories = specific_categories[1:]
        # check if any news are turned off
        false_in_specific_categories = False in specific_categories

        if key == "all" and not false_in_specific_categories:
            for key, _ in marked[country].items():
                marked[country][key] = False
            await theme_manager.set_interests(interests=marked, user_id=user_id)

        elif key == "all" and False in specific_categories:
            for key, _ in marked[country].items():
                marked[country][key] = True
            await theme_manager.set_interests(interests=marked, user_id=user_id)

        elif key != "all" and false_in_specific_categories:
            marked[country]["all"] = False
            await theme_manager.set_interests(interests=marked, user_id=user_id)

        elif key != "all" and not false_in_specific_categories:
            marked[country]["all"] = True
            await theme_manager.set_interests(interests=marked, user_id=user_id)

        keyboard = await keyboard_themes(marked, language, country)

        country_name: str = lang_manager.country_to_name[language][country] + lang_manager.country_to_emoji[country]
        text: str = str(lang_manager.phrases[language]["choose_themes"]).format(country_name)

        bot_message = await bot.edit_message_text(chat_id=user_id, message_id=previous_message_id, text=text, reply_markup=keyboard)
        bot_message_id = bot_message["message_id"]

        await dp.storage.update_data(chat=user_id, data_to_pass=[bot_message_id, language])


async def hello_message(message: types.message, state: FSMContext):
    await bot.answer_callback_query(message.id)

    user_id = message.from_user.id
    previous_data = dict(await dp.storage.get_data(chat=user_id))["data_to_pass"]
    previous_message_id = previous_data[0]
    language = previous_data[1]

    await bot.delete_message(chat_id=user_id, message_id=previous_message_id)

    subscribed_themes: dict = await theme_manager.subscribed_themes(user_id=user_id)

    if len(subscribed_themes) == 0:
        text = lang_manager.phrases[language]["no_theme"]
    else:
        text = lang_manager.phrases[language]["these_themes"]

        for country, themes in subscribed_themes.items():
            country_emoji = lang_manager.country_to_emoji[country]
            country_name = lang_manager.country_to_name[language][country]

            text += "<b>{}</b> {}:\n".format(country_name, country_emoji)

            for theme in themes:
                theme_name = theme_manager.theme_translates[language][country][theme]
                text += "▫️ <i>{}</i>\n".format(theme_name)

    await bot.send_message(chat_id=user_id, text=text)
    await state.finish()


def register_handlers_settings(dp: Dispatcher):
    dp.register_message_handler(process_hi_command, text=['Назад'])
    dp.register_message_handler(process_hi_command, commands=["start"], state=None)
    dp.register_callback_query_handler(choose_language, lambda c: c.data.startswith('choose_lang_'),
                                       state=FSMcreate.choose_language)
    dp.register_callback_query_handler(choose_themes, lambda c: c.data.startswith('choose_country_'),
                                       state=FSMcreate.choose_country)
    dp.register_callback_query_handler(choose_themes, lambda c: c.data.startswith('choose_theme_'),
                                       state=FSMcreate.choose_themes)
    dp.register_callback_query_handler(choose_language, lambda c: c.data.startswith('back_to_countries'),
                                       state=FSMcreate.choose_themes)
    dp.register_callback_query_handler(hello_message, lambda c: (c.data == 'continue_to_menu'), state=FSMcreate.choose_country)
