import asyncio
import threading
import time

import schedule

from config import admin_id, alert_channel_id
from create_bot import bot, dp, tg_posts_manager
from aiogram import executor

from db.models import create_tables
from ParserMain import background_parsing
from AnalyzerMain import background_analyzer



loop = asyncio.get_event_loop()
loop.create_task(background_parsing())
loop.create_task(background_analyzer())


async def start_whole_systems(dp):
    await create_tables()

    for i in admin_id:
        await bot.send_message(chat_id=i, text="Bot was started")
    await bot.send_message(chat_id=alert_channel_id, text="Bot was started")

# def task():
#     print("Task is completed!")
#
# def scheduling_task():
#     schedule.every(3).seconds.do(task)
#
#     while True:
#         schedule.run_pending()
#
#         sleep(1)
#
#
# thread_1 = threading.Thread(target=scheduling_task)
# thread_1.start()

from handlers import settings, admin

settings.register_handlers_settings(dp)
admin.register_handlers_create(dp)

executor.start_polling(dp, on_startup=start_whole_systems, skip_updates=True)
