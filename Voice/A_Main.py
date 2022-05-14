import ftplib
import os
import sys
import random
import time
import socket
from playsound import playsound
import speech_recognition as speech_r
import pyaudio
import wave
import cv2
from loguru import logger
import paho.mqtt.client as mqtt
from setupF import cmnd
from haarcascade import HaarCascade
from setupF import ftpOwn

logger.add("setupF/debug.log", format="| {time} | {level} | {message}", colorize=True) 
word = []
message_complete = ''


def receiving_message_complete(client, userdata, msg):
    global message_complete
    message_complete = msg.payload.decode()
    print(message_complete)

def record_audio():
    global word
    flag = 1
    while flag == 1:
        if os.path.isfile('frame.jpg') == True:
            p = pyaudio.PyAudio()
            stream = p.open(format=cmnd.FRT,channels=cmnd.CHAN,rate=cmnd.RT,
                           input=True,frames_per_buffer=cmnd.CHUNK) 

            logger.debug("Started recording")
            frames = [] 
            for i in range(0, int(cmnd.RT / cmnd.CHUNK * cmnd.REC_SEC)):
                data = stream.read(cmnd.CHUNK)
                frames.append(data)
            logger.debug("Done")

            stream.stop_stream(); stream.close();p.terminate()
            w = wave.open("output.wav", 'wb')
            w.setnchannels(cmnd.CHAN); w.setsampwidth(p.get_sample_size(cmnd.FRT)); w.setframerate(cmnd.RT)
            w.writeframes(b''.join(frames)); w.close()
            sample = speech_r.WavFile('output.wav')
            flag = 0
            r = speech_r.Recognizer()

            with sample as audio:
                try:
                    content = r.record(audio)
                    voice_ouput = r.recognize_google(audio_data=content, language="ru-RU")
                    word = voice_ouput.split(' ')
                    logger.debug(word)
                    flag=0
                except speech_r.UnknownValueError:
                    logger.error('Ничего не было сказано')
                    playsound("files/audio/file_repeat.mp3")
                    flag=1
                    pass
    detect_mood()

def detect_mood():
    is_happyOrSad = ''
    for i in word:
        for a in cmnd.sad_array:
            if i == a:
                if b.message == "S":
                    playsound("files/audio/file_S.mp3")
                    time.sleep(1)
                    #Добавить предложение рассказать шутку
                    client.publish("tomatocoder/report","S")
                    logger.debug("Sad")
                    playsound(f"files/audio/{cmnd.audio_jokes[random.randint(0,2)]}.mp3")
                    return None
                else:
                    playsound("files/audio/file_mood.mp3")
                    record_audio()
                    pass
            else:
                is_happyOrSad += i
                # pass
                #Добавить наводящие вопросы 

        for a in cmnd.happy_array:
            if i == a:
                if b.message == "H":
                    playsound("files/audio/file_H.mp3")
                    client.publish("tomatocoder/report","H")
                    logger.debug("Happy")
                else:
                    playsound("files/audio/file_mood.mp3") 
                    record_audio()
            else:
                is_happyOrSad += i
                #Добавить наводящие вопросы 

    if is_happyOrSad != '':
        logger.debug("Didn't find Sad or Happy")
        playsound("files/audio/file_mood.mp3") 
        is_happyOrSad=''
        record_audio()

def mainActions():
    global message_complete
    while True:
        while message_complete != "1":
            time.sleep(5)
        message_complete = ""

        b.main()
        playsound("files/audio/file_wazup.mp3")
        record_audio()

        client.publish(cmnd.topic_report_readiness, "R")
        client.publish(cmnd.topic_go, "b")

        ftp.uploadFile("output.wav")
        logger.debug("uploaded AUDIO")
        ftp.uploadFile("frame.jpg")
        logger.debug("UPLOADED PHOTO")

        cv2.destroyAllWindows()
        cv2.waitKey(1)

try:
    ftp = ftpOwn.FtpOwn()
    ftp.ftpConnect("213.226.112.19", 21)

    client = mqtt.Client()
    client.username_pw_set("tomatocoder", "Coder_tomato1")
    client.connect("mqtt.pi40.ru", 1883)
    client.subscribe(cmnd.topic_complete)
    client.subscribe(cmnd.topic_go)
    client.message_callback_add(cmnd.topic_complete, receiving_message_complete)
    client.loop_start()
    
    cap=cv2.VideoCapture(0)
    b = HaarCascade(cap)

    mainActions()

except KeyboardInterrupt as e:
        logger.error(f"Произошла ошибка: {e}")
        ftp.quitFile()
    
except socket.timeout as e:
        logger.error(f"Произошла ошибка: {e}")
        ftp.quitFile()

except socket.gaierror as e:
        logger.error(f"Произошла ошибка: {e}")
        ftp.quitFile()

except ftplib.error_temp as e:
        logger.error(f"Произошла ошибка: {e}")
        ftp.ftpConnect("213.226.112.19", 21)
        ftp.uploadFile("output.wav")
        logger.debug("uploaded AUDIO")
        ftp.uploadFile("frame.jpg")
        logger.debug("UPLOADED PHOTO")
        mainActions()


