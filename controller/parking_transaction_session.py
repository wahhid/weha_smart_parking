import requests
from return_handling import ReturnHandling
from db import DBHelper
from datetime import datetime
from lib.data.api_urls import ApiEndPoint

class ParkingTransactionSession(DBHelper):

    def __init__(self, controller):
        super(ParkingTransactionSession,self).__init__(controller)

    def create(self, vals):
        try:
            headers = {
                'access-token': self.controller.access_token
            }
            
            payload = {
                #'pos_session_id': pos_session_id,           
                "booth_id": vals['booth_id'],
                "operator_id": vals['operator_id']
            }


            response = requests.post('http://park-dev.server008.weha-id.com' + ApiEndPoint.parking_session, headers=headers, data=payload)
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
        