from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from create_bot import lang_manager

keyboard_choose_lang = InlineKeyboardMarkup(row_width=3)
for lang in lang_manager.country_to_emoji.keys():
    if lang in lang_manager.langs:
        emoji = lang_manager.country_to_emoji[lang]
        button = InlineKeyboardButton(text=emoji, callback_data=f"choose_lang_{lang}")
        keyboard_choose_lang.add(button)




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



admin_key = ReplyKeyboardMarkup(resize_keyboard=True).add(button_add_user, button_delete_user).add(button_check_user, button_check_all).add(button_prices, button_delete_price, button_add_price).add(button_send_all, button_send_one).add(button_cancel)
