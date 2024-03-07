from aiogram.types import (ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,
                           InlineKeyboardButton)

from create_bot import lang_manager, theme_manager, user_lang_manager


async def keyboard_choose_lang():
    keyboard = InlineKeyboardMarkup(row_width=3)
    for lang in lang_manager.country_to_emoji.keys():
        if lang in lang_manager.langs:
            emoji = lang_manager.country_to_emoji[lang]
            button = InlineKeyboardButton(text=emoji, callback_data=f"choose_lang_{lang}")
            keyboard.add(button)

    return keyboard


async def keyboard_countries(user_id: int, state: int):
    # get user language
    language: str = (await user_lang_manager.get(user_id)).language_interface
    # get all countries to get news
    countries: list = list(theme_manager.theme_translates[language].keys())
    keyboard = InlineKeyboardMarkup(row_width=3)

    # separate world button from all countries
    world_emoji = lang_manager.country_to_emoji["world"]
    countries.remove("world")

    world_button = InlineKeyboardButton(text=f"{world_emoji} {lang_manager.country_to_name[language]['world']}",
                                        callback_data="choose_country_world")
    # add world button in first row
    keyboard.row(world_button)

    # add buttons with countries to keyboard
    for country in countries:
        emoji = lang_manager.country_to_emoji[country]

        text = f"{emoji} {lang_manager.country_to_name[language][country]}"

        button = InlineKeyboardButton(text=text, callback_data=f"choose_country_{country}")
        keyboard.add(button)

    if state == 2:
        next_text = lang_manager.phrases[language]["next"]
        next_button = InlineKeyboardButton(text=next_text, callback_data="continue_to_menu")

        keyboard.row(next_button)

    return keyboard


async def keyboard_themes(marked_themes: dict, language: str, country: str):
    # define general keyboard
    keyboard = InlineKeyboardMarkup(row_width=2, resize_keyboard=True)

    themes = theme_manager.theme_translates[language][country]

    keys = themes.keys()
    translates = themes.values()

    items = list(themes.items())[1:]

    marked_themes = marked_themes[country]

    if not (False in list(marked_themes.values())[1:]) and (not marked_themes["all"]):
        all_button = InlineKeyboardButton(text=themes["all"] + " - ✅", callback_data=f"choose_theme_{country}_all")
    elif marked_themes["all"]:
        all_button = InlineKeyboardButton(text=themes["all"] + " - ✅", callback_data=f"choose_theme_{country}_all")
    else:
        all_button = InlineKeyboardButton(text=themes["all"], callback_data=f"choose_theme_{country}_all")

    # add buttons
    for key, translate in items:
        if marked_themes["all"] or marked_themes[key]:
            text = f"{translate} ✅"
        else:
            text = translate
        call = f"choose_theme_{country}_{key}"

        button = InlineKeyboardButton(text=text, callback_data=call)
        keyboard.insert(button)

    back_translate = lang_manager.phrases[language]["back"]
    back_text = f"{back_translate} ↩️"
    back_button = InlineKeyboardButton(text=back_text, callback_data="back_to_countries")

    keyboard.row(all_button)
    keyboard.row(back_button)

    # elif marked_themes[]:
    #
    #
    return keyboard

check_new_channels = KeyboardButton("re-check channels")
back_to_start = KeyboardButton("Back")

admin_main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(
    check_new_channels,
    back_to_start
)





button_cancel = KeyboardButton('Назад')

button_complete = KeyboardButton('Готово✅')
complete_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_complete).add(button_cancel)

brcs_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_cancel)

button_spot = KeyboardButton('Обробка')
button_faq = KeyboardButton('FAQ📜')

# greet_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_spred_p2p_spot, button_courses_spot).row(button_courses_p2p, button_allp2p).row(button_subscribe)
greet_key = ReplyKeyboardMarkup(resize_keyboard=True).row(button_spot, button_faq)

button_add_user = KeyboardButton('Додати')
button_delete_user = KeyboardButton('Видалити')
button_check_user = KeyboardButton('Перевірити інфо')
button_check_all = KeyboardButton('Список акаунтів')
button_prices = KeyboardButton('Ключі')
button_delete_price = KeyboardButton('Видалити ключ')
button_add_price = KeyboardButton('Додати ключ')
button_send_all = KeyboardButton('Розіслати текст')
button_send_one = KeyboardButton('Надіслати текст')

admin_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_user, button_delete_user).add(button_check_user,
                                                                                                   button_check_all).add(
    button_prices, button_delete_price, button_add_price).add(button_send_all, button_send_one).add(button_cancel)
