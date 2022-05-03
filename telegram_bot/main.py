import asyncio
import ftplib
from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger
import paho.mqtt.client as mqtt

from app.config_reader import load_config
from app.handlers.check_retiree import register_check_retiree
from app.handlers.common import register_handlers_common
from app.handlers.report import register_handlers_report


async def main():
    logger.info("Starting bot")

    config = load_config('config/main.ini')
    

    bot = Bot(token = config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot)
    client = mqtt.Client()

    logger.add("debug.log", format=" {time} {message}") 
  
    register_handlers_common(dp)
    register_check_retiree(dp)
    register_handlers_report(dp)

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
    
