from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QLabel, QListView, QScrollArea, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot, Qt, QThread

import sys
import cv2
import os
from return_handling import ReturnHandling
from lib.ui import ParentUi
import numpy as np



class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)


class ParkingOperatorClientUi(ParentUi):

    ui_path = "ui/p0003.ui"

    def __init__(self, controller):
        super(ParkingOperatorClientUi, self).__init__(controller)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.display_width = self.image_label.frameGeometry().width()
        print(self.display_width)
        self.display_height = self.image_label.frameGeometry().height()
        print(self.display_height)
        self.LoginLabel.setText(self.controller.username)
        self.LoginLabel.setProperty('class', 'message_border')
        self.ShowLabel.setProperty('class', 'message_border')
        self.CommandLabel.setProperty('class', 'message_border')
        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()
        self.load_session()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def initButton(self):
        super(ParkingOperatorClientUi, self).init_button()
        self.ExitButton.setProperty('class','big_button')
        self.ExitButton.clicked.connect(self.exitButtonPressed)

    def load_session(self):
        vals = {
            'booth_id':  2,
            'operator_id': 2,
        }
        returnHandling = self.controller.parkingTransactionSessionController.create(
            vals)
        if returnHandling.err:
            msg = QMessageBox.about(self, "Warning", returnHandling.message)
        self.controller.session = returnHandling.data
        self.SessionLabel.setText(returnHandling.data['name'])

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            if len(self.CommandLabel.text()) == 0:
                pass
            else:
                dialog = QtWidgets.QInputDialog(self)
                dialog.resize(QtCore.QSize(500, 100))
                dialog.setWindowTitle('Pricing Dialog')
                # dialog.setModal(True)
                dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
                dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)
                dialog.setLabelText('Barcode:')
                items = ("Car", "Motor Cylce", "Taxi", "Truck")
                dialog.setComboBoxItems(items)
                # dialog.setStyleSheet(
                #   """
                #     QComboBox {
                #       font-size: 24pt;
                #       border: 2px solid black;
                #       border-color: #ffc107;
                #       color: rgb(96, 97, 97);
                #     }
                #     QPushButton { 
                #         color: #ffffff;
                #         background-color: #ffc107;
                #         border-width: 1px;
                #         color: rgb(96, 97, 97);
                #         border-style: solid;
                #         border-radius: 3;
                #         padding: 3px;
                #         padding-left: 5px;
                #         padding-right: 5px; 
                #         width: 60px;
                #         height: 40px;
                #       }
                #       QPushButton:pressed{
                #         color :rgb(96, 97, 97);
                #         background-color: #ffffff;
                #         border-width: 1px;
                #         border-color: : rgb(96, 97, 97);
                #         border-style: solid;
                #         border-radius: 3;
                #         padding: 3px;
                #         padding-left: 5px;
                #         padding-right: 5px;
                #       }
                #   """)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    item = dialog.textValue()
                    self.PricingLabel.setText(item)
                    print(item)
                    print(self.CommandLabel.text())
                    self.ShowLabel.setText(self.CommandLabel.text())
                    dialog = QtWidgets.QInputDialog(self)
                    dialog.resize(QtCore.QSize(500, 100))
                    dialog.setWindowTitle('Scan Barcode Dialog')
                    dialog.setLabelText('Barcode:')
                    dialog.setTextEchoMode(QtWidgets.QLineEdit.Normal)
                    # dialog.setStyleSheet(
                    #     """QPushButton { 
                    #             color: #ffffff;
                    #             background-color: #ffc107;
                    #             border-width: 1px;
                    #             color: rgb(96, 97, 97);
                    #             border-style: solid;
                    #             border-radius: 3;
                    #             padding: 3px;
                    #             padding-left: 5px;
                    #             padding-right: 5px; 
                    #             width: 60px;
                    #             height: 40px;
                    #         }

                    #         QLineEdit {
                    #             font-size:24pt; 
                    #             border: 2px solid black;
                    #             border-color: #ffc107;
                    #             color: rgb(96, 97, 97);
                    #         }
                    #         QLabel {
                    #             font-size:24pt;
                    #         }
                    #     """)
                    if dialog.exec_() == QtWidgets.QDialog.Accepted:
                        barcode_value = dialog.textValue()
                        # Send Pre-Exit
                        vals = {
                            'trans_id': barcode_value,
                            'plat_number': self.CommandLabel.text(),
                            'exit_booth_id': 2,
                            'exit_operator_id': 1,
                            'parking_session_id': self.controller.session['id'],
                        }
                        print(vals)
                        returnHandling = self.controller.parkingTransactionController.pre_exit(
                            vals)
                        if returnHandling.err:
                            print("Eror Pre Exit")
                            msg = QMessageBox.about(
                                self, "Warning", returnHandling.message)
                        else:
                            self.CommandLabel.setText("")
                    else:
                        print("Cancel")
                        self.CommandLabel.setText("")
                else:
                  print("Cancel Pricing Dialog")
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.CommandLabel.setText(self.CommandLabel.text()[:-1])
        else:
            self.CommandLabel.setText(
                self.CommandLabel.text() + event.text().upper())

    def exitButtonPressed(self):
        self.controller.unload_parking_operator_client()
