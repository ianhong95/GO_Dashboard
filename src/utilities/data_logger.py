import os
import json
import dotenv
import time
import logging

from metrolinx_api.gtfs_vehicle_position import GtfsVehiclePosition
from metrolinx_api.general_data_fetcher import GeneralDataFetcher
from postgres_interface import PostgresInterface

class DataLogger():
    def __init__(self):
        self.vehicle_data = GtfsVehiclePosition()
        self.general_data = GeneralDataFetcher()

        self.db = PostgresInterface(
            SERVER_IP=self.general_data.SERVER_IP,
            DATABASE_NAME=self.general_data.DB_NAME,
            USER=self.general_data.DB_USER,
            PASSWORD=self.general_data.DB_PASSWORD
        )

        self.data = self.vehicle_data.get_all_data()

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("DataLogger initialized")

    def log_all_vehicles(self):
        vehicles = self.vehicle_data.get_all_vehicle_info()
        
        for vehicle_id, vehicle_info in vehicles.items():
            self.logger.debug(f'Parsing data in {vehicle_info}')

            timestamp = vehicle_info['timestamp']
            vehicle_label = vehicle_info['label']
            latitude = vehicle_info['latitude']
            longitude = vehicle_info['longitude']
            trip_id = vehicle_info['trip_id']
            vehicle_type = vehicle_info['type']
            route = vehicle_info['route']
            terminal_dest = vehicle_info['terminal_dest']

            self.db.add_row_to_vehicle_info(
                timestamp,
                int(vehicle_id), 
                vehicle_label,
                latitude,
                longitude,
                trip_id,
                vehicle_type,
                route,
                terminal_dest
            )

            self.logger.debug(f'Wrote data to "vehicle_info" table.')

    def log_all_trips(self):
        trips = self.vehicle_data.get_trip_info()

        for trip_id, trip_info in trips.items():
            self.logger.debug(f'Parsing data in {trip_info}')

            timestamp = trip_info['timestamp']
            route_id = trip_info['route_id']
            direction = str(trip_info['direction_id'])
            trip_start_time = trip_info['trip_start_time']
            trip_start_date = trip_info['trip_start_date']
            schedule_relationship = trip_info['schedule_relationship']
            stop_id = trip_info['stop_id']
            current_status = trip_info['current_status']

            self.db.add_row_to_trip_info(
                timestamp, trip_id, route_id, direction, trip_start_time, trip_start_date, schedule_relationship, stop_id, current_status
            )

            self.logger.debug(f'Wrote data to "trip_info" table.')


    def log_all_stop_info(self):
        '''Only need to run this once to pull all basic stop info. Takes about 15 minutes to run.'''
        stops = self.general_data.get_all_stop_info()

        for stop_code, stop_info in stops.items():
            print(f'Adding stop code {stops[stop_code]}')
            print(f'Adding stop_info from {stop_info}')
            self.db.add_row_to_stops(
                stop_code,
                stop_info['stop_name'],
                stop_info['location_name'],
                stop_info['latitude'],
                stop_info['longitude'],
                stop_info['is_train'],
                stop_info['is_bus']
            )


def main():
    logging.basicConfig(
        filename='src/logs/data_logger.log',
        level=logging.CRITICAL,  # change to DEBUG for more detail
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    data_logger = DataLogger()

    while True:
        data_logger.vehicle_data.update_data()
        data_logger.log_all_vehicles()
        data_logger.log_all_trips()

        # Avoid spamming Metrolinx
        time.sleep(10)


if __name__=='__main__':
    main()