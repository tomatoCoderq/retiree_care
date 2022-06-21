from aiogram import types, Dispatcher
import keyboards
from loguru import logger
import sqlite3
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

import keyboards


class CodeInput(StatesGroup):
    waitingForAnswer = State()

async def start(message:types.Message):
    await message.answer(f"""Привет, <b>{message.from_user.full_name}!</b>Я - система <b>Retiree-Care</b>🤖 
Система <b>Retiree-Care</b> позволяет людям <i>всегда</i> быть на связе со своими пожилыми родственниками.""", reply_markup=types.ReplyKeyboardRemove(True))
    logger.info("Greetings were sent")
    await message.answer(f"Для того чтобы продолжить использовать нашу систему, вам надо ввести код, который находится на коробке!")
    await CodeInput.waitingForAnswer.set()

async def get_answer(message:types.Message, state:FSMContext):
    if message.text == "010122":
        await message.reply(f"Отлично! Приятного пользования!", reply_markup=keyboards.keyboard_main())
    elif message.is_command:
        await message.reply(f"Вы неверно ввели код! Попробуйте еще раз!")
    else:
        await message.reply(f"Вы неверно ввели код! Попробуйте еще раз!")
        return

def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", "hello", "welcome", "about", "проведать"])
    dp.register_message_handler(get_answer, state=CodeInput.waitingForAnswer)