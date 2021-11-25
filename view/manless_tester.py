from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout, QPlainTextEdit
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    
import sys
import os
import base64
import codecs
from functools import partial
from datetime import datetime
import hashlib
from escpos.printer import Usb
from . import *

from dotenv import load_dotenv
import os

import re
import serial
import time
import threading 
import gtts
from playsound import playsound
from lib.errorhandling import ErrorHandling
from lib.libmanless import ManlessDevice

class ManlessTester(QWidget):

    def __init__(self, app_path):
        super(ManlessTester, self).__init__()
        self.app_path = app_path
        self.threads = list()
        load_dotenv(verbose=True)
        ui_path = os.path.join(self.app_path, "ui/q0001-400x300.ui")
        self.ser = serial.Serial('/dev/cu.usbmodem14201', 9600, timeout=1)
        self.data = ""
        self.CAR_DETECTED = False
        self.greeting = True
        uic.loadUi(ui_path, self)
        self.initUi()
    
    def initUi(self):
        self.ConnectPushButton.clicked.connect(self.connectPushButtonPressed)
        self.DisconnectPushButton.clicked.connect(self.disconnectPushButtonPressed)

    def disconnectPushButtonPressed(self):
        self.device.terminate()

    def connectPushButtonPressed(self):
        self.device = ManlessDevice()
        self.device.start()
        # while True:
        #     receive = self.ser.read()
        #     self.data = self.data + receive.decode('utf-8')
        #     if len(self.data) == 4:
        #         print(self.data)
        #         if self.data == "1000":
        #             print("CAR DETECTED")
        #             CAR_DETECTED = True
        #             if self.greeting:
        #                 print("Run Greeting")
        #                 greeting = False
        #                 x = threading.Thread(target=self.thread_function, args=(1,))
        #                 x.start()
        #         if self.data == "2000":
        #             print("ENTRY BUTTON PRESSED")
        #             time.sleep(5)
        #             self.create_transaction()
        #             self.greeting = True
        #         if self.data == "8001":
        #             print("CAR NOT DETECTED")
        #             CAR_DETECTED = False
        #         if self.data == "8002":
        #             print('RESET DEVICE')
        #             self.greeting = True
        #         self.data = ""

    def setMessage(self, message):
        self.MessageLabel.setText(message)

    def clearGreeting(self):
        print("Clearing")
        greeting = True

    def thread_function(self,name):
        tts = gtts.gTTS("Selamat Datang di Mal Taman Anggrek, Tekan Tombol atau Tap Kartu Langganan Anda", lang="id")
        tts.save("hola.mp3")
        playsound("hola.mp3")
        #time.sleep(10000)
        self.clearGreeting()

    def create_transaction(self):
        print("Create Transaction")
        self.ser.write("8000".encode())


    
