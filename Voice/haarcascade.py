import cv2
from loguru import logger
import numpy as np
import os
from playsound import playsound
import time
from ftpOwn import FtpOwn


class HaarCascade():
    message = ""

    def __init__(self,video):
        self.video=video
        self.ftp = FtpOwn()
        self.ftp.ftpConnect("213.226.112.19", 21)

    def detect_face(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10)
        if len(faces) == 0:
            return None, None
        (x, y, w, h) = faces[0]
        return gray[y:y + w, x:x + h], faces[0]

    def prepare_training_data(self):
        dirs = os.listdir('img_train/')
        faces = []
        labels = []
        for image_path in dirs:
            if image_path[0] == 'h':
                label = 1
            else:
                label = 2

            image_path = './img_train/' + image_path
            image = cv2.imread(image_path)
            face, rect = self.detect_face(image)
            if face is not None:
                faces.append(face)
                labels.append(label)

        return faces, labels

    def draw_text(self,img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    def draw_rectangle(self,img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def predict(self,test_img, face_recognizer):
        subjects = ['None', 'Happy', 'Sad']
        label_text = ''
        img = test_img.copy()

        face, rect = self.detect_face(img)

        if face is not None:
            label = face_recognizer.predict(face)
            label_text = subjects[label[0]]
            self.draw_rectangle(img, rect)
            self.draw_text(img, label_text, rect[0], rect[1] - 5)


        return img, label_text
    def main(self):        
        logger.debug("Подготовка папок...")
        faces, labels = self.prepare_training_data()
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces, np.array(labels))
        logger.debug("Подготовка изображений для обучения...")
        text_old = ''
        is_face = True 
        count = 0

        while count < 50:
            print(is_face)
            isRead, image = self.video.read()
            face, rect = self.detect_face(image)
            predicted_img1, b = self.predict(image, face_recognizer)
            cv2.imshow("screen", predicted_img1)
            key = cv2.waitKey(1)
            if face is not None:
                count += 1
                is_face=False
        cv2.destroyWindow("screen")
        
        os.remove("frame.jpg")
        cv2.imwrite("frame.jpg", predicted_img1)
        self.ftp.uploadFile("frame.jpg")
        logger.debug("UPLOADED PHOTO")
        if face is not None:
            a, label_text = self.predict(image, face_recognizer)
            if text_old == '':
                text_old = label_text
                if label_text == 'Sad':
                    print('Sad')
                    playsound("files/audio/audio_Sad.mp3", True)
                    text_old = label_text
                    self.message = "S"
                    time.sleep(3)
                elif label_text == 'Happy':
                    print('Happy')
                    playsound("files/audio/audio_Happy.mp3", True)
                    text_old = label_text
                    self.message = "H"
                    time.sleep(3)
                else:
                    pass
            else:
                if label_text == text_old:
                    pass
                else:
                    if label_text == 'Sad':
                        print('Sad')
                        playsound("files/audio/audio_Sad.mp3", True)
                        text_old = label_text
                        self.message = "S"
                        time.sleep(3)
                    elif label_text == 'Happy':
                        print('Happy')
                        playsound("files/audio/audio_Happy.mp3", True)
                        text_old = label_text
                        self.message = "H"
                        time.sleep(3)
                    else:
                        pass
        cv2.destroyAllWindows()
        self.video.release()