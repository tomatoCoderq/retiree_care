from loguru import logger 
from aiogram import types, Dispatcher
from paho.mqtt import client
from aiogram.dispatcher.filters import Text


import keyboards
import cmd

client = client.Client()
client.username_pw_set("tomatocoder", "Coder_tomato1")
client.connect("mqtt.pi40.ru", 1883)
client.subscribe(cmd.go_topic)#топик отправки


async def check(message:types.Message):
    client.loop_start()
    client.publish(cmd.go_topic, "Go")
    await message.reply("<b>Робот выехал с зарядной станции!</b> Через некоторое время вы сможете посмотреть отчёт", reply_markup=keyboards.keyboard_main())
    logger.info(f"Отправил GO на топик {cmd.go_topic}")

def register_check_retiree(dp:Dispatcher):
    dp.register_message_handler(check, Text(equals=cmd.button1))