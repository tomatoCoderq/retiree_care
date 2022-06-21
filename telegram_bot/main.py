import asyncio
from aiogram import Bot, types, Dispatcher
from loguru import logger
import paho.mqtt.client as mqtt
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from app.config_reader import load_config
from app.handlers.check_retiree import register_check_retiree
from app.handlers.common import register_handlers_common
from app.handlers.report import register_handlers_report


message_complete = ''

def receiving_message_complete(client, userdata, msg):
    global message_complete
    message_complete = msg.payload.decode()

async def main():
    logger.info("Starting bot")

    config = load_config('config/main.ini')

    bot = Bot(token = config.tg_bot.token, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    client = mqtt.Client()
    client.username_pw_set("tomatocoder", "Coder_tomato1")
    client.connect("mqtt.pi40.ru", 1883)

    logger.add("debug.log", format=" {time} {message}") 
  
    register_handlers_common(dp)
    register_check_retiree(dp)
    register_handlers_report(dp)

    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
    
