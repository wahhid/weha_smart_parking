import requests
from return_handling import ReturnHandling
from db import DBHelper
from datetime import datetime
from lib.data.api_urls import ApiEndPoint

class Parking(DBHelper):

    def __init__(self, controller):
        super(Parking, self).__init__(controller)


    def 