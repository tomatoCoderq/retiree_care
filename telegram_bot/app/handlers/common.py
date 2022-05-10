from aiogram import types, Dispatcher
import keyboards
from loguru import logger


async def start(message:types.Message):
    await message.answer(f"""Привет, <b>{message.from_user.full_name}!</b>Я - система <b>Retiree-Care</b>🤖 
Система <b>Retiree-Care</b> позволяет людям <i>всегда</i> быть на связе со своими пожилыми родственниками.""", reply_markup=keyboards.keyboard_main())
    logger.info("Greetings were sent")

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "hello", "welcome", "about", "проведать"])
