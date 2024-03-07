from aiogram import Bot, Dispatcher

from ParserMain import ParserMain
from config import token
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

from language import LanguageManager
from theme import ThemeManager

from db.UserUtils import UserUtils
from db.UserLanguageUtils import UserLanguageUtils
from db.UserInterestsUtils import UserInterestsUtils
from db.TGChannelsUtils import TGChannelsUtils
from db.TGPostsUtils import TGPostsUtils
from db.OpenAiKeyUtils import OpenAiKeyUtils

logging.basicConfig(format='[+] %(asctime)s | %(message)s', datefmt='%d-%b %H:%M:%S', level=logging.INFO)

storage = MemoryStorage()

# define all DB managers
db_client = UserUtils()
user_manager = UserUtils()
user_lang_manager = UserLanguageUtils()


loop = asyncio.get_event_loop()
lang_manager = LanguageManager(user_lang_manager)
interests_manager = UserInterestsUtils()
theme_manager = ThemeManager(interests_manager=interests_manager, lang_manager=lang_manager)
tg_channels_manager = TGChannelsUtils()
tg_posts_manager = TGPostsUtils()
parser_main = ParserMain()
openai_key_manager = OpenAiKeyUtils()


bot = Bot(token, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage=storage)
