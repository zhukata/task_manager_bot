import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from middlewares.db import DataBaseSession
load_dotenv()

from database.engine import create_db, drop_db, session_maker
from handlers.user_private import user_private_router
from handlers.admin_private import admin_router
from bot_cmd_list import private


# ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=os.getenv('TOKEN'),default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.user_tokens = {}

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(admin_router)

 
async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()
    print('бот работает')


async def on_shutdown(bot):
    print('бот лег')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    

asyncio.run(main())