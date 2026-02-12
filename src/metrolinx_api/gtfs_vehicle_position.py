import httpx
import json

from metrolinx_api.general_data_fetcher import GeneralDataFetcher

class GtfsVehiclePosition(GeneralDataFetcher):
    '''
    The purpose of this class is to take the massive response from the live vehicle position API call
    and rearrange it into smaller useful chunks.
    '''
    def __init__(self):
        super().__init__('Gtfs.json/Feed/VehiclePosition')

        self.update_data()

    def update_data(self):
        # Fetch data
        self.raw_data = self.get_all_data()

        # Separate the header and data for ease of access
        self.header = self.raw_data['header']
        self.data = self.raw_data['entity']

    def extract_timestamp(self) -> str:
        return self.header['timestamp']
    
    def get_all_vehicle_info(self) -> dict:

        vehicle_info = {vehicle['vehicle']['vehicle']['id']: {
            'timestamp': self.header['timestamp'],
            'label': vehicle['vehicle']['vehicle']['label'],
            'latitude': vehicle['vehicle']['position']['latitude'],
            'longitude': vehicle['vehicle']['position']['longitude'],
            'trip_id': vehicle['vehicle']['trip']['trip_id']
            }
            for vehicle in self.data
        }

        for vehicle in vehicle_info.values():
            vehicle['type'], vehicle['route'], vehicle['terminal_dest'] = self.get_vehicle_type_by_label(vehicle['label'])

        return vehicle_info
    
    
    def get_trip_info(self) -> dict:
        
        trip_info = {vehicle['vehicle']['trip']['trip_id']: {
            'timestamp': self.header['timestamp'],
            'route_id': vehicle['vehicle']['trip']['route_id'],
            'direction_id': vehicle['vehicle']['trip']['direction_id'],
            'trip_start_time': vehicle['vehicle']['trip']['start_time'],
            'trip_start_date': vehicle['vehicle']['trip']['start_date'],
            'schedule_relationship': vehicle['vehicle']['trip']['schedule_relationship'],
            'stop_id': vehicle['vehicle']['stop_id'],
            'current_status': vehicle['vehicle']['current_status']
            }
            for vehicle in self.data
        }

        return trip_info
    

    def get_vehicle_type_by_label(self, label: str):
        """
        Extracts granular information from vehicle label. The first part is the code,
        and the second part is the terminal destination. If the code contains numbers,
        the vehicle is a bus. If not, it is a train.
        """
        if label:
            split_label = label.split(' - ')
            route_code = split_label[0]
            terminal_dest = split_label[1]

            if any(char.isdigit() for char in route_code):
                vehicle_type = 'bus'
            elif not any(char.isdigit() for char in route_code):
                vehicle_type = 'train'
            else:
                vehicle_type = 'unknown'

            return vehicle_type, route_code, terminal_dest

        else:
            return 'unknown', '', ''