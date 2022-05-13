import time
import asyncio
from loguru import logger 
from aiogram import types, Dispatcher
import paho.mqtt.client as mqtt
from aiogram.dispatcher.filters import Text
import keyboards
import cmd


message_complete = ""
message_report_readiness = ""
background_message = ""


def receiving_message_complete(client, userdata, msg):
    global message_complete
    message_complete = msg.payload.decode()
    print(message_complete)    

def receiving_message_report_readiness(client, userdata, msg):
    global message_report_readiness
    message_report_readiness = msg.payload.decode()

async def check(message:types.Message):
    global is_True, is_S, background_message
    client = mqtt.Client()
    client.username_pw_set("tomatocoder", "Coder_tomato1")
    client.connect("mqtt.pi40.ru", 1883)
    client.subscribe(cmd.go_topic)
    client.subscribe(cmd.topic_report_readiness)
    client.subscribe(cmd.topic_complete)
    client.message_callback_add(cmd.topic_complete, receiving_message_complete)
    client.message_callback_add(cmd.topic_report_readiness, receiving_message_report_readiness)
    client.loop_start()

    client.publish(cmd.go_topic, "Go")

    # asyncio.create_task(background_waiting_for_complete())

    background_message = message
    await message.reply("<b>Робот выехал с зарядной станции!</b> Через некоторое время вы сможете посмотреть отчёт", reply_markup=keyboards.keyboard_main())
    logger.info(f"Отправил GO на топик {cmd.go_topic}")

# async def background_waiting_for_complete():
#     if message_complete == "1":
#         print("!!!!")
#         await background_message.answer("<b>Робот доехал!</b> Ожидайте свой отчёт, я сообщу, когда вы сможете его посмотреть.")
#     elif message_report_readiness == "0":
#         await background_message.answer(f"<b>Ваш отчёт готов!</b> Вы можете посмотреть его, нажав на кнопку <i>{cmd.button2}</i>.")    


    #         if message_report_readiness == "R":
    #             await message.answer(f"<b>Ваш отчёт готов!</b> Вы можете посмотреть его, нажав на кнопку <i>{cmd.button2}</i>.")    
    #             is_True = False
    #         time.sleep(1)
    # except(KeyboardInterrupt):
    #     is_True = False 

def register_check_retiree(dp:Dispatcher):
    dp.register_message_handler(check, Text(equals=cmd.button1))