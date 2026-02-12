import httpx
import json
import os
import time
from dotenv import load_dotenv

FUNCTIONS = {
    'stops': 'Stop.json/All',
    'stop_details': 'Stop.json/Details',    # Need a stop code
}

class GeneralDataFetcher():
    '''
    Base class for general HTTP methods.
    '''
    def __init__(self, API_METHOD: str = ""):
        load_dotenv()

        self.URL = os.getenv('ENDPOINT_URL')
        self.API_KEY= os.getenv('API_KEY')
        self.API_METHOD = API_METHOD
        self.SERVER_IP = os.getenv('SERVER_IP')
        self.DB_USER=os.getenv('DB_USER')
        self.DB_PASSWORD=os.getenv('DB_PASSWORD')
        self.DB_NAME=os.getenv('DB_NAME')

    def send_get_request(self, api_method: str):
        '''Helper function to send http requests.'''

        r = httpx.get(f'{self.URL}/{api_method}?key={self.API_KEY}', timeout=300.0)
        return r


    def get_all_data(self) -> dict:
        r = self.send_get_request(self.API_METHOD)

        return r.json()
    
    def get_stops(self) -> dict:
        r = self.send_get_request(FUNCTIONS['stops'])
        stops_json = r.json()

        stops = {stop["LocationCode"]: stop["LocationName"] for stop in stops_json['Stations']['Station']}
        
        return stops
    
    def get_all_stop_info(self) -> dict:
        '''
        This method only needs to run once because stop info is static. It's only used
        to populate the "stops" table in the database.
        '''
        stops = self.get_stops()

        stop_details = {}

        for code, location in stops.items():
            r = self.send_get_request(f'{FUNCTIONS["stop_details"]}/{code}')
            stops_json = r.json()
            stop_res_body = stops_json['Stop']

            stop_details[code] = {
                'location_name': location,
                'stop_name': stop_res_body['StopName'],
                'latitude': stop_res_body['Latitude'],
                'longitude': stop_res_body['Longitude'],
                'is_bus': stop_res_body['IsBus'],
                'is_train': stop_res_body['IsTrain']
            }

            print(f'New stop code: {code}')
            print(f'New stop info: {stop_details[code]}')

            # Space out requests to avoid spamming server
            time.sleep(1)

        return stop_details
