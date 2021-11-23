from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSize    
import sys
import os
import cv2
import threading
import queue
from return_handling import ReturnHandling
from lib.ui import ParentUi
from printer.receipt_entry import ReceiptEntry
running = False
capture_thread = None
q = queue.Queue()

def grab(cam, queue, width, height, fps):
   global running
   capture = cv2.VideoCapture(cam)
   capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
   capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
   capture.set(cv2.CAP_PROP_FPS, fps)

   while(running):
      frame = {}        
      capture.grab()
      retval, img = capture.retrieve(0)
      frame["img"] = img

      if queue.qsize() < 10:
            queue.put(frame)
      else:
            print(queue.qsize())

class OwnImageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()




class ParkingManlessClientUi(ParentUi):

   ui_path = "ui/p0002.ui"

   def __init__(self, controller):
      super(ParkingManlessClientUi, self).__init__(controller)
      self.init_button()
      self.auto_login()
      self.receiptEntry = ReceiptEntry()

      self.window_width = self.ImgWidget.frameSize().width()
      self.window_height = self.ImgWidget.frameSize().height()
      self.ImgWidget = OwnImageWidget(self.ImgWidget)       

      self.timer = QtCore.QTimer(self)
      self.timer.timeout.connect(self.update_frame)
      self.timer.start(1)

      global running
      running = True
      capture_thread = threading.Thread(target=grab, args = (0, q, 1920, 1080, 30))
      #capture_thread.start()
      

   def initButton(self):
      super(ParkingManlessClientUi, self).init_button()
      self.EntryButton.clicked.connect(self.entryButtonPressed)

   def auto_login(self):
      print('AutoLogin')
      username = os.getenv('MANLESS_USERNAME')
      password = os.getenv('MANLESS_PASSWORD')
      returnHandling = self.controller.resUsersController.api_login('park-dev', username, password)
      if returnHandling.err:
         msg = QMessageBox.about(self, "Warning", returnHandling.message)

      else:       
         data = returnHandling.data
         #Update Global Controller
         self.controller.is_login = True
         self.controller.access_token = data['access_token']
         self.controller.logger.info("Login as " + os.getenv('MANLESS_USERNAME'))
         self.controller.username = username
         self.controller.password = password
         self.controller.uid = data['uid']
         self.controller.pos_session = False
         self.controller.company_id = data['company_id']

   def entryButtonPressed(self):
      vals = {
         'entry_booth_id': 1,
         'is_member': 0,
         'barcode': '',
         'input_method': 'manless',
         'entry_operator_id': 1, 
      }
      returnHandling = self.controller.parkingTransactionController.entry(vals)
      if returnHandling.err:
         msg = QMessageBox.about(self, "Warning", returnHandling.message)
      else:       
         data = returnHandling.data
         print(data)
         self.TransactionList.addItem(data[0]['name'])
         self.receiptEntry.print(data[0])
   

   def update_frame(self):
      if not q.empty():
         self.startButton.setText('Camera is live')
         frame = q.get()
         img = frame["img"]

         img_height, img_width, img_colors = img.shape
         scale_w = float(self.window_width) / float(img_width)
         scale_h = float(self.window_height) / float(img_height)
         scale = min([scale_w, scale_h])

         if scale == 0:
               scale = 1
         
         img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
         height, width, bpc = img.shape
         bpl = bpc * width
         image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
         self.ImgWidget.setImage(image)