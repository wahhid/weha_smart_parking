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

class ManlessTester(QWidget):

    def __init__(self, app_path):
        super(ManlessTester, self).__init__()
        self.app_path = app_path
        self.threads = list()
        load_dotenv(verbose=True)
        ui_path = os.path.join(self.app_path, "ui/q0001-400x300.ui")
        uic.loadUi(ui_path, self)
        self.initUi()
    
    def initUi(self):
        self.ConnectPushButton.clicked.connect(self.connectPushButtonPressed)

    def connectPushButtonPressed(self):
        result = self.flazzReader.connect()
        if result.err:
            print(result.message)
        else:
            print(result.message)
        
        self.setMessage(result.message)

    def setMessage(self, message):
        self.MessageLabel.setText(message)
        


    
