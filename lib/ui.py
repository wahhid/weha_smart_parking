from PyQt5 import QtWidgets, QtCore, QtSvg, uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
from return_handling import ReturnHandling


class ParentUi(QtWidgets.QWidget):

    window_title = ''

    def __init__(self, controller):
        super(ParentUi, self).__init__()
        self.controller = controller
        self.app_path = controller.app_path
        self.init_ui()
        self.initButton()
      
    def init_ui(self):
        ui_path = os.path.join(self.app_path, self.ui_path)
        uic.loadUi(ui_path, self)
        self.setWindowTitle(self.window_title)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        effect = QtWidgets.QGraphicsDropShadowEffect(self)
        effect.setOffset(20, 30)
        effect.setBlurRadius(20)
        self.setGraphicsEffect(effect)

    def init_button(self):
        pass