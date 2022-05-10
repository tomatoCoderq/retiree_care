from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger
import cmd 


def keyboard_main():
    buttons = [types.KeyboardButton(text=cmd.button1),
    types.KeyboardButton(text=cmd.button2)]
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(*buttons)
    return keyboard