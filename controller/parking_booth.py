import requests
from return_handling import ReturnHandling
from db import DBHelper
from datetime import datetime
from lib.data.api_urls import ApiEndPoint

class ParkingBooth(DBHelper):

        def __init__(self, controller):
                super(ParkingBooth,self).__init__(controller)


        def get_by_code(self, code):
                headers = {
                        'Authorization': 'Bearer ' + self.controller.access_token
                }
                response = requests.post('http://park-dev.server008.weha-id.com' + ApiEndPoint.parking_booth_by_code + "/" + code, headers=headers)
                if response.status_code != 200:
                        print(response.status_code)
                        return ReturnHandling(True, "Booth not found" , False)
                
                response_json  = response.json()
                if response_json['err']:
                        return ReturnHandling(True, response_json['message'] , False)
                
                return ReturnHandling(False, "", response_json['data'])

                