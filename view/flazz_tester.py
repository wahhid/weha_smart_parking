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
import threading
import time
from lib.errorhandling import ErrorHandling
from lib.libbcaflazz import BcaFlazzLibrary

class FlazzTester(QWidget):

    def __init__(self, app_path):
        super(FlazzTester, self).__init__()
        self.app_path = app_path
        self.threads = list()
        load_dotenv(verbose=True)
        ui_path = os.path.join(self.app_path, "ui/FlazzTester.ui")
        uic.loadUi(ui_path, self)
        self.flazzReader = BcaFlazzLibrary('/dev/tty.UC-232AC',  38400, timeout=10)
        self.initUi()
    
    def initUi(self):
        self.connectPushButton = self.findChild(QPushButton, 'ConnectPushButton')
        self.connectPushButton.clicked.connect(self.connectPushButtonPressed)
        self.signOnPushButton = self.findChild(QPushButton, 'SignOnPushButton')
        self.signOnPushButton.clicked.connect(self.signOnPushButtonPressed)
        self.paymentPushButton = self.findChild(QPushButton, 'PaymentPushButton')
        self.paymentPushButton.clicked.connect(self.paymentPushButtonPressed)
        self.exitPushButton = self.findChild(QPushButton, 'ExitPushButton')
        self.exitPushButton.clicked.connect(self.exitPushButtonPressed)
        self.messageTextEdit = self.findChild(QPlainTextEdit, 'MessageTextEdit')

    def connectPushButtonPressed(self):
        result = self.flazzReader.connect()
        if result.err:
            print(result.message)
        else:
            print(result.message)
        
        self.setMessage(result.message)


    def signOnPushButtonPressed(self):
        result = self.flazzReader.signon()
        if result.err:
            self.setMessage(result.message)
        else:
            self.setMessage(result.message)
        

    def paymentPushButtonPressed(self):
        result = self.flazzReader.payment()
        if result.err:
            self.setMessage(result.message)
        else:
            self.setMessage(result.message)

    def exitPushButtonPressed(self):
        print("Exit Clicked")

    def setMessage(self, message):
        self.messageTextEdit.appendPlainText(message)
        


    
