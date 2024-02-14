from config import admin_id, alert_channel_id
from create_bot import bot, dp
from aiogram import executor


async def send_admin(dp):
    for i in admin_id:
        await bot.send_message(chat_id=i, text="Bot was started")
    await bot.send_message(chat_id=alert_channel_id, text="Bot was started")


from handlers import settings, admin

settings.register_handlers_settings(dp)
admin.register_handlers_create(dp)

executor.start_polling(dp, on_startup=send_admin, skip_updates=True)
