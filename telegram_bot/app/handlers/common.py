from aiogram import types, Dispatcher
import logging 
import keyboards
from loguru import logger



async def start(message:types.Message):
    await message.answer(f"""Привет, <b>{message.from_user.full_name}!</b>
Привет, я система <b>Retiree-Care</b>. 
Мы позволяем людям <i>всегда</i> быть на связе со своими пожилыми родственниками.""", reply_markup=keyboards.keyboard_main())
    logger.info("MESSAGE WITH GREETINGS WAS SENT")

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "hello", "welcome", "about"])
