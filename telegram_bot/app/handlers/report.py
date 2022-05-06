from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from loguru import logger
from socket import timeout
import paho.mqtt.client as mqtt
import cmd
from ftpOwn import FtpOwn


message_report = ''
async def report(message:types.Message):
    try:
        ftp = FtpOwn()
        ftp.ftpConnect("213.226.112.19", 21)
        ftp.downloadFile("frame.jpg", "photo_audio/frame.jpg")
        ftp.downloadFile("output.wav", "photo_audio/output.wav")

        client = mqtt.Client()
        client.username_pw_set("tomatocoder", "Coder_tomato1")
        client.connect("mqtt.pi40.ru", 1883)
        client.subscribe("tomatocoder/report")
        client.loop_start()
        client.message_callback_add("tomatocoder/report", receiving_message_report)
        if message_report == "S":
            logger.debug("SAD")
        else:
            logger.debug("HAPPY")

        photo = open('photo_audio/frame.jpg', 'rb')
        logger.debug(f"opened PHOTO file")
        audio = open('photo_audio/output.wav', 'rb')
        logger.debug(f"opened AUDIO file")

        await message.answer("""Ваш отчёт: 
        
        """)
        await message.answer_photo(photo=photo)
        await message.answer_audio(audio=audio)
        logger.info(f"Send photo and audio")
    except (timeout, KeyboardInterrupt):
        ftp.quitFile()
        

def receiving_message_report(client, userdata, msg):
    global message_report
    message_report = msg.payload.decode()

def register_handlers_report(dp:Dispatcher):
    dp.register_message_handler(report, Text(equals=cmd.button2))
