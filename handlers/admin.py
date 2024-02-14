from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard import greet_key, brcs_key, admin_key
# from api import count_from_api
import datetime as DT
from time import sleep
import xlsxwriter

async def admin_start(message: types.Message):
	await bot.send_message(chat_id=-1001551885182, text=f'<i>LOG-Admin panel--!</i>\n{message.from_user}\n<b>Цей адмін увійшов в адмін панель</b>')
	await FSMcreate.admin_panel.set()
	await bot.send_message(chat_id = message.from_user.id, text = "Вітаю👋\nЦе зручна адмін панель в якій ти можеш керувати підписки користувачів.\n\n<b>\"Додати\"</b><i> - відповідає за додавання підписки користувачу</i>\n<b>\"Видалити\"</b><i> - відповідає за видалення підписки користувача з бд</i>\n<b>\"Перевірити інфо\"</b><i> - перевірка часу користувач</i>а\n<b>\"Список акаунтів\"</b><i> - Виводить абсолютно всіх підписки користувачів</i>\n\nУсі функції перераховані нижче😉" , reply_markup=admin_key)

async def back(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	elif str(current_state) in ["FSMcreate:add_user", "FSMcreate:del_user", "FSMcreate:check_user", "FSMcreate:delete_price", "FSMcreate:add_price", "FSMcreate:tbmain", "FSMcreate:send_all_main"]:
		await FSMcreate.admin_panel.set()
		await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=admin_key)
		return
	else:
		await state.finish()
		await bot.send_message(chat_id = message.from_user.id, text = 'Ok', reply_markup=greet_key)
		return

def register_handlers_create(dp: Dispatcher):
    dp.register_message_handler(back, state='*', commands=['Назад'])
    dp.register_message_handler(back, Text(equals='назад', ignore_case=True), state='*')