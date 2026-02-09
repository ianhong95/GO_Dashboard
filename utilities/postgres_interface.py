'''
Docstring for utilities.postgres_interface
'''

import psycopg as ps
import sys

class PostgresInterface():
    def __init__(
            self,
            SERVER_IP: str,
            DATABASE_NAME: str,
            USER: str,
            PASSWORD: str,
            PORT: int = 5432
    ):
        
        self.SERVER_IP = SERVER_IP
        self.DATABASE_NAME = DATABASE_NAME
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.PORT = PORT

        self._connect(self.SERVER_IP, self.DATABASE_NAME, self.USER, self.PASSWORD, self.PORT)


    def _connect(
            self,
            SERVER_IP: str,
            DATABASE_NAME: str,
            USER: str,
            PASSWORD: str,
            PORT: int=5432
    ):
        try:
            print(f'Connecting to database {DATABASE_NAME} at {SERVER_IP}:{PORT} as user {USER}...')
            
            self.conn = ps.connect(f'postgresql://{USER}:{PASSWORD}@{SERVER_IP}:{PORT}/{DATABASE_NAME}', autocommit=True)
            
            # Change the search path (it defaults to the public schema)
            with self.conn.cursor() as cursor:
                cursor.execute(f"ALTER USER {self.USER} SET search_path TO transit_data, public")
            
            print(f'Connected!')

        except ps.Error as e:
            print(e)
            sys.exit(0)


    def add_row_to_vehicle_info(
            self,
            timestamp: int,
            vehicle_id: int,
            vehicle_label: str,
            latitude: float,
            longitude: float,
            trip_id: str,
            vehicle_type: str,
            route: str,
            terminal_dest: str
    ):
        with self.conn.cursor() as cursor:
            query = """
                INSERT INTO vehicle_info (
                    api_timestamp,
                    vehicle_id,
                    vehicle_label,
                    latitude,
                    longitude,
                    trip_id,
                    vehicle_type,
                    route,
                    terminal_dest
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (
                timestamp,
                vehicle_id,
                vehicle_label,
                latitude,
                longitude,
                trip_id,
                vehicle_type,
                route,
                terminal_dest
                )
            )

    def add_row_to_stops(
            self,
            stop_id: str,
            stop_name: str,
            location_name: str,
            latitude: float,
            longitude: float,
            train_station: bool,
            bus_station: bool
    ):
        with self.conn.cursor() as cursor:
            query = '''
                INSERT INTO transit_data.stops (
                    stop_id, stop_name, location_name, latitude, longitude, train_station, bus_station
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            '''

            cursor.execute(query, (
                stop_id,
                stop_name,
                location_name,
                latitude,
                longitude,
                train_station,
                bus_station
                )
            )

    def add_row_to_trip_info(
            self,
            timestamp: int,
            trip_id: str,
            route_id: str,
            direction: int,
            trip_start_time: str,
            trip_start_date: str,
            schedule_relationship: str,
            stop_id: str,
            current_status: str
    ):
        with self.conn.cursor() as cursor:
            query = """
                INSERT INTO trip_info (
                    api_timestamp,
                    trip_id,
                    route_id,
                    direction,
                    trip_start_time,
                    trip_start_date,
                    schedule_relationship,
                    stop_id,
                    current_status
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                timestamp,
                trip_id,
                route_id,
                direction,
                trip_start_time,
                trip_start_date,
                schedule_relationship,
                stop_id,
                current_status
                )
            )