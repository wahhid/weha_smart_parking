from PyQt5 import QtWidgets, QtCore, uic
#from PyQt5.QtGui import QIcon, QPixmap
from view.flazz_tester import FlazzTester

import sys
import os
import qdarkstyle

app = QtWidgets.QApplication(sys.argv)
app_path = os.path.dirname(os.path.abspath(__file__))
flazzTesterUi = FlazzTester(app_path)
flazzTesterUi.show()
app.exec_()