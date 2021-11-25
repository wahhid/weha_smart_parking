from PyQt5 import QtWidgets, QtCore, uic
#from PyQt5.QtGui import QIcon, QPixmap
#from view.flazz_tester import FlazzTester
from view.manless_tester import ManlessTester

import sys
import os
#import qdarkstyle

app = QtWidgets.QApplication(sys.argv)
app_path = os.path.dirname(os.path.abspath(__file__))
manlessTesterUi = ManlessTester(app_path)
manlessTesterUi.show()
app.exec_()