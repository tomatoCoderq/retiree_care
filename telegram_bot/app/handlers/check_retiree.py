import time
import asyncio
from loguru import logger 
from aiogram import types, Dispatcher
import paho.mqtt.client as mqtt
from aiogram.dispatcher.filters import Text
import keyboards
import cmnd


message_complete = ""
message_report_readiness = ""
background_message = ""
goComplete = ""


def receiving_message_complete(client, userdata, msg):
    global message_complete
    message_complete = msg.payload.decode()
    # print(message_complete)    

def receiving_message_report_readiness(client, userdata, msg):
    global message_report_readiness
    message_report_readiness = msg.payload.decode()

async def check(message:types.Message):
    global background_message, goComplete
    client = mqtt.Client()
    client.username_pw_set("tomatocoder", "Coder_tomato1")
    client.connect("mqtt.pi40.ru", 1883)
    client.subscribe(cmnd.go_topic)
    client.subscribe(cmnd.topic_report_readiness)
    client.subscribe(cmnd.topic_complete)
    client.message_callback_add(cmnd.topic_complete, receiving_message_complete)
    client.message_callback_add(cmnd.topic_report_readiness, receiving_message_report_readiness)
    client.loop_start()

    # asyncio.create_task(background_waiting_for_complete())

    # if goComplete == "101":
    client.publish(cmnd.go_topic, "Go")
    #     goComplete = ""
    # if goComplete == "":
    #     await message.answer("Вы уже вызывали робота недавно. Подождите, скоро он доедет!")

    background_message = message
    await message.reply("<b>Робот выехал с зарядной станции!</b> Через некоторое время вы сможете посмотреть отчёт", reply_markup=keyboards.keyboard_main())
    logger.info(f"Отправил GO на топик {cmnd.go_topic}")

async def background_waiting_for_complete():
    if message_complete == "1":
        logger.debug(message_complete)
        Go_complete = "101"
#     if message_complete == "1":
#         print("!!!!")
#         await background_message.answer("<b>Робот доехал!</b> Ожидайте свой отчёт, я сообщу, когда вы сможете его посмотреть.")
#     elif message_report_readiness == "0":
#         await background_message.answer(f"<b>Ваш отчёт готов!</b> Вы можете посмотреть его, нажав на кнопку <i>{cmnd.button2}</i>.")    


    #         if message_report_readiness == "R":
    #             await message.answer(f"<b>Ваш отчёт готов!</b> Вы можете посмотреть его, нажав на кнопку <i>{cmnd.button2}</i>.")    
    #             is_True = False
    #         time.sleep(1)
    # except(KeyboardInterrupt):
    #     is_True = False 

def register_check_retiree(dp:Dispatcher):
    dp.register_message_handler(check, Text(equals=cmnd.button1))