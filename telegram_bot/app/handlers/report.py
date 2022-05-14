from aiogram import types, Dispatcher
import socket
from aiogram.dispatcher.filters import Text
from loguru import logger
from socket import timeout
import paho.mqtt.client as mqtt
import cmnd
from ftpOwn import FtpOwn


message_report = ''
message_nuero = ''
pulse = ''
brain_activity = ''
var = ''


def receiving_message_report(client, userdata, msg):
    global message_report
    message_report = msg.payload.decode()

def receiving_message_nuero(client, userdata, msg):
    global message_nuero
    message_nuero = msg.payload.decode()

# def retiree_status():
#     global pulse, brain_activity
#     if len(message_nuero) < 4:
#         pass
#     else:
#         brain_activity = message_nuero[0:2]
#         pulse = message_nuero[2:]
#         if int(pulse) > 75 and int(pulse) < 85:
#             pass
#         elif int(pulse)< 75:
#             print("too low")
#         else:
#             print("too high")


async def report(message:types.Message):
    global pulse, brain_activity
    try:
        ftp = FtpOwn()
        ftp.ftpConnect(cmnd.ip, 21)
        ftp.downloadFile("frame.jpg", "photo_audio/frame.jpg")
        ftp.downloadFile("output.wav", "photo_audio/output.wav")

        client = mqtt.Client()
        client.username_pw_set("tomatocoder", "Coder_tomato1")
        client.connect("mqtt.pi40.ru", 1883)
        client.subscribe(cmnd.topic_report)
        client.subscribe(cmnd.topic_neuro_modules)
        client.message_callback_add(cmnd.topic_report, receiving_message_report)
        client.message_callback_add(cmnd.topic_neuro_modules, receiving_message_nuero)
        client.loop_start()

        photo = open('photo_audio/frame.jpg', 'rb')
        logger.debug(f"opened PHOTO file")
        audio = open('photo_audio/output.wav', 'rb')
        logger.debug(f"opened AUDIO file")

        if len(message_nuero) >= 4:
            brain_activity = message_nuero[0:2]
            pulse = message_nuero[2:] 

            await message.answer(f"""Ваш отчёт: 
            Пульс пенсионера - {pulse}
            Мозговая активность - {brain_activity}""")
            await message.answer_photo(photo=photo)
            await message.answer_audio(audio=audio)
            logger.info(f"Send photo and audio")
        
        else:
            await message.answer("<b>Подождите!</b> Нейродатчики ещё не распознали пульс активность головного мозга!")

    except (timeout, KeyboardInterrupt, socket.gaierror) as e:
        logger.error(f"Произошла ошибка: {e}")
        ftp.quitFile()

def register_handlers_report(dp:Dispatcher):
    dp.register_message_handler(report, Text(equals=cmnd.button2))
