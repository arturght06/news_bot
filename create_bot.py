from aiogram import Bot, Dispatcher
from config import token
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

from language import LanguageManager
from database import *

logging.basicConfig(format='[+] %(asctime)s | %(message)s', datefmt='%d-%b %H:%M:%S', level=logging.INFO)

storage = MemoryStorage()

db_client = db_utils.DBUtils()
lang_manager = LanguageManager(db_client)

loop = asyncio.get_event_loop()
bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage=storage)
