from PyQt5 import QtWidgets, QtCore, uic
import sys
import os
import logging 
from configparser import ConfigParser
from dotenv import load_dotenv
# View

# Controller
#from controller.res_users import ResUsers as ResUserController
#from controller.parking_transaction import ParkingTransaction as ParkingTransactionController
#from controller.parking_transaction_session import ParkingTransactionSession as ParkingTransactionSessionController
#from controller.parking_booth import ParkingBooth as ParkingBoothController
from controller.parking import Parking as ParkingController


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Controller():

    is_login = False
    access_token = None
    ui_type = 'q'
    booth = False
    
    def __init__(self, app_path):
        super(Controller, self).__init__()
        load_dotenv(verbose=True)
        self.config_object = ConfigParser()
        self.config_object.read("config.ini")
        self.logger = logging.getLogger(__name__)

        #Init Value

        #Init Controller
        self.parkingController = ParkingController(self)

    def load_ui(self):
        pass
        
    def load_login(self):     
        if self.ui_type == 'p':   
            from view.p.parking_login import ParkingLoginUi

            self.parkingLoginUi = ParkingLoginUi(self)
            self.parkingLoginUi.show()

    def load_parking_manless_client(self):
        if self.ui_type == 'p':   
            from view.p.parking_manless_client import ParkingManlessClientUi

            self.parkingManlessClientUi = ParkingManlessClientUi(self)
            self.parkingManlessClientUi.show()
        
        if self.ui_type == 'q':
               

    def load_parking_operator_client(self):
        if os.getenv('UI_TYPE') == 'p':   
            from view.p.parking_operator_client import ParkingOperatorClientUi

            self.parkingOperatorClientUi = ParkingOperatorClientUi(self)
            self.parkingOperatorClientUi.show()

    def load_pos_command(self):
        if self.pos_type == 'q':
            from lib.view.q.pos_command import PosCommandUi
            self.posCommandUi = PosCommandUi(self)
            self.posLoginUi.close()
            self.posCommandUi.show()

    def load_pos_order(self):
        if self.pos_type == 'p':
            from lib.view.pos_order import PosOrderUi
            self.posOrderUi = PosOrderUi(self)
            self.posCommandUi.close()
            self.posOrderUi.show()

        if self.pos_type == 'q':
            from lib.view.q.pos_order import PosOrderUi
            self.posOrderUi = PosOrderUi(self)
            self.posCommandUi.close()
            self.posOrderUi.show()        

    def load_pos_order_line(self):
        if self.pos_type == 'q':
            from lib.view.q.pos_order_line import PosOrderLineUi
            self.posOrderLineUi = PosOrderLineUi(self)
            self.posOrderLineUi.show()

    def load_pos_payment(self):
        if self.pos_type == 'p':
            from lib.view.pos_payment import PosPaymentUi
            self.posPaymentUi = PosPaymentUi(self)
            self.posOrderUi.setEnabled(False)
            self.posPaymentUi.show()
        
        if self.pos_type == 'q':
            from lib.view.q.pos_payment import PosPaymentUi
            self.posPaymentUi = PosPaymentUi(self)
            self.posOrderUi.setEnabled(False)
            self.posPaymentUi.show()

    def load_pos_customer(self):
        self.posCustomerUi = PosCustomerUi(self)
        self.posOrderUi.setEnabled(False)
        self.posCustomerUi.show()

    def load_pos_promo(self):
        self.posPromotionUi = PosPromotionUi(self)
        self.posOrderUi.setEnabled(False)
        self.posPromotionUi.show()

    def load_pos_product(self):
        pass 

    def unload_pos_command(self):
        self.posCommandUi.close()
        self.posLoginUi.show()

    def unload_parking_operator_client(self):
        self.parkingOperatorClientUi.close() 

    def unload_pos_order(self):
        self.posOrderUi.close()
        self.posCommandUi.show()
    
    def unload_pos_order_line(self):
        self.posOrderLineUi.close()
        self.posOrderUi.show()

    def unload_pos_payment(self):
        self.posPaymentUi.close()
        self.posOrderUi.setEnabled(True)
        self.posOrderUi.show()
    
    def unload_pos_customer(self):
        self.posCustomerUi.close()
        self.posOrderUi.setEnabled(True)
    
    def unload_pos_promotion(self):
        self.posPromotionUi.close()
        self.posOrderUi.setEnabled(True)

    def logout(self):
        self.posOrderUi.close()
        self.posLoginUi.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    #apply_stylesheet(app, theme='dark_teal.xml')
    app_path = os.path.dirname(os.path.abspath(__file__))
    
    
    #stylesheet = app.styleSheet()
    # app.setStyleSheet(stylesheet + "QPushButton{color: red; text-transform: none;}")
    with open( app_path + '/style/custom.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

   
    controller = Controller(app_path)
    controller.load_ui()
    if os.getenv('BOOTH_TYPE')  == 'manless':
        controller.load_parking_manless_client()
    else:
        controller.load_login()
    

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()