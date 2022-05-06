import cv2
import os
from playsound import playsound
import speech_recognition as speech_r
import pyaudio
import wave
from loguru import logger
import paho.mqtt.client as mqtt
import cmd
from haarcascade import HaarCascade
from ftpOwn import FtpOwn

logger.add("debug.log", format=" {time} {message}") 
word = []


def record_audio():
    global word
    flag = 1
    while flag == 1:
        if os.path.isfile('frame.jpg') == True:
            p = pyaudio.PyAudio()
            stream = p.open(format=cmd.FRT,channels=cmd.CHAN,rate=cmd.RT,
                           input=True,frames_per_buffer=cmd.CHUNK) 

            logger.debug("Started recording")
            frames = [] 
            for i in range(0, int(cmd.RT / cmd.CHUNK * cmd.REC_SEC)):
                data = stream.read(cmd.CHUNK)
                frames.append(data)

            logger.debug("Done")
            stream.stop_stream(); stream.close()
            p.terminate()
            w = wave.open("output.wav", 'wb')
            w.setnchannels(cmd.CHAN); w.setsampwidth(p.get_sample_size(cmd.FRT)); w.setframerate(cmd.RT)
            w.writeframes(b''.join(frames));w.close()
            sample = speech_r.WavFile('output.wav')
            flag = 0
            r = speech_r.Recognizer()

            with sample as audio:
                try:
                    content = r.record(audio)
                    voice_ouput = r.recognize_google(audio_data=content, language="ru-RU")
                    word = voice_ouput.split(' ')
                    flag=0
                except speech_r.UnknownValueError:
                    logger.error('Ничего не было сказано')
                    playsound("files/audio/file_repeat.mp3")
                    flag=1
                    pass
    detect_mood()

def detect_mood():
    for i in word:
        for a in cmd.sad_array:
                if i == a:
                    if b.message == "S":
                        playsound("files/audio/file_S.mp3")
                        client.publish("tomatocoder/report","S")
                        
                        logger.debug("Sad")
                    else:
                        playsound("files/audio/file_mood.mp3")
                        record_audio()
        for a in cmd.happy_array:
            if i == a:
                if b.message == "H":
                    playsound("files/audio/file_H.mp3")
                    client.publish("tomatocoder/report","H")
                    logger.debug("Happy")
                else:
                    playsound("files/audio/file_mood.mp3") 
                    record_audio()



ftp = FtpOwn()
ftp.ftpConnect("213.226.112.19", 21)
client = mqtt.Client()
client.username_pw_set("tomatocoder", "Coder_tomato1")
client.connect("mqtt.pi40.ru", 1883)
cap=cv2.VideoCapture(0)
b = HaarCascade(cap)

#---MAIN---#
b.main()
playsound("files/audio/file_wazup.mp3")
record_audio()
# detect_mood()

ftp.uploadFile("output.wav")
logger.debug("uploaded AUDIO")



