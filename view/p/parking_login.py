from PyQt5 import QtWidgets, QtCore, QtSvg, uic, QtGui
from PyQt5.QtGui import QIcon, QPixmap
import sys
import os
from return_handling import ReturnHandling
from lib.ui import ParentUi

class ParkingLoginUi(ParentUi):

    ui_path = "ui/p0001.ui"

    def __init__(self, controller):
        super(ParkingLoginUi, self).__init__(controller)

    def initButton(self):
        super(ParkingLoginUi, self).init_button()

        self.ExitButton.clicked.connect(self.exitButtonPressed)
        self.LoginButton.clicked.connect(self.loginButtonPressed)
        self.EmailEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)
        self.PasswordEdit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, False)

    def load_booth(self):
        returnHandling = self.controller.parkingBoothController.get_by_code(os.getenv('BOOTH_CODE'))
        if returnHandling.err:
            print("Load Booth Error")
            print(returnHandling.message)
            self.BoothLabel.setText(returnHandling.message)
        self.controller.booth = returnHandling.data 
        
    def exitButtonPressed(self):
      self.close()
    
    def getSession(self, user_id):
      returnHandling = self.posSess

    def loginButtonPressed(self):
      print('Login Button Pressed')
      returnHandling = self.controller.resUsersController.api_login('park-dev', self.EmailEdit.text(), self.PasswordEdit.text())
      if returnHandling.err:
        self.showError(returnHandling.message)
        self.clearUi()
      else:
        print(returnHandling.message)

        #Update Global Controller
        username = self.EmailEdit.text()
        password = self.PasswordEdit.text()
        data = returnHandling.data
        self.controller.is_login = True
        self.controller.access_token = data['access_token']
        self.controller.logger.info("Login as " + username)
        self.controller.username = username
        self.controller.password = password
        self.controller.uid = data['uid']
        self.controller.pos_session = False
        self.controller.company_id = data['company_id']   
        self.clearUi() 
        self.load_booth()
        print(os.getenv("BOOTH_TYPE"))
        print(type(os.getenv("BOOTH_TYPE")))
        if os.getenv("BOOTH_TYPE") == "manless":
            print("Load Manless UI")
            self.controller.load_parking_manless_client()       
        if os.getenv("BOOTH_TYPE") == "operator":
            print("Load Operator UI")
            self.controller.load_parking_operator_client()       

    def emailNumpadButtonPressed(self):
      self.setEnabled(False)
      #self.exPopup = numberPopup(self, self.emailEdit, "", self.callBackOnSubmit, "Argument 1", "Argument 2")
      #self.exPopup.setGeometry(130, 320,400, 300)
      #self.exPopup.show()
      keyboard = AlphaNeumericVirtualKeyboard(self.emailEdit)
      keyboard.display(ui_Scroll=False)
    
    def showError(self, message):
        self.MessageLabel.setText(message)

    def clearUi(self):
        self.EmailEdit.setText("")
        self.PasswordEdit.setText("")
        self.EmailEdit.setFocus(True)
  
    def callBackOnSubmit(self, arg1, arg2): 
      print("Function is called with args: %s & %s" % (arg1, arg2))

    def onClick(self,e):
        self.setEnabled(True)