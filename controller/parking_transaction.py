import requests
from return_handling import ReturnHandling
from db import DBHelper
from datetime import datetime
from lib.data.api_urls import ApiEndPoint

class ParkingTransaction(DBHelper):

    def __init__(self, controller):
        super(ParkingTransaction,self).__init__(controller)

    
    def entry(self, vals):
        try:
            headers = {
                'access-token': self.controller.access_token
            }
            
            payload = {          
                "entry_booth_id": vals['entry_booth_id'],
                "is_member": vals['is_member'],
                "barcode": vals['barcode'],
                "input_method": vals['input_method'],
                "entry_operator_id": vals['entry_operator_id'],
            }

            response = requests.post('http://park-dev.server008.weha-id.com' + ApiEndPoint.parking_entry, headers=headers, data=payload)
            if response.status_code != 200:
                print(response.status_code)
                return ReturnHandling(True, "Error Create" , False)
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                 return ReturnHandling(True, response_json['message'], [])
            return ReturnHandling(False, "", response_json['data'])
        except Exception as err:
            print(err)
            return ReturnHandling(True, str(err), [])
        

    def pre_exit(self, vals):
        try:
            headers = {
                'access-token': self.controller.access_token
            }
            

            payload={
                'trans_id': vals['trans_id'],
                'plat_number': vals['plat_number'],
                'exit_booth_id': vals['exit_booth_id'],
                'exit_operator_id': vals['exit_operator_id'],
                'parking_session_id': vals['parking_session_id']
            }
            
            response = requests.post('http://park-dev.server008.weha-id.com' + ApiEndPoint.parking_pre_exit, headers=headers, data=payload)
            if response.status_code != 200:
                print(response.status_code)
                return ReturnHandling(True, "Error Create" , False)
            response_json  = response.json()
            print(response_json)
            if response_json['err'] == True:
                 return ReturnHandling(True, response_json['message'], [])
            return ReturnHandling(False, "", response_json['data'])
        except Exception as err:
            print(err)
            return ReturnHandling(True, str(err), [])

    def post_exit(self, vals):
        pass 