from loguru import logger 
from ftplib import FTP, FTP_TLS

class FtpOwn():
    def __init__(self):
        self.ftp = FTP()

    '''Функция ftpConnect позволяет подключить к серверу(Внимание!Не забудьте включить сервер сперва). Принимает: 
        ip(ip-адрес сервера. Пример 127.0.0.1)
        port(ввести порт. Пример 1026)
        folder(Путь к папке. К папке должен быть с сервера. Пример Server(Папка внутри папки, в которой запущен сервер))'''
    def ftpConnect(self, ip, port):
        self.ftp.set_pasv(False)
        self.ftp.connect(ip, port)
        self.ftp.login("testuser", "test")
        logger.info(self.ftp.retrlines('LIST'))
        logger.debug(f"CONNECTED TO {ip, port} ")

    '''Функция downloadFile позволяет скачать файл из папки, к которой вы обратились в ftpconnect. Принимает:
       file_name(имя файла. Пример output.wav)
       path(путь, куда запишется файл)'''
    def downloadFile(self, file_name, path):
        with open(f"{path}", 'wb') as f:
            self.ftp.retrbinary('RETR ' + f"{file_name}", f.write)  
            logger.info(f"DOWNLOADED FROM FTP-SERVER FILE {file_name}")
    
    '''Функция uploadFile позволяет загрузить файл в папку, к которой вы обращались в ftpconnect. Принимает:
       file_name(имя файла. Пример output.wav)'''
    def uploadFile(self,file_name):
        self.ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))

    def quitFile(self):
        self.ftp.quit()

